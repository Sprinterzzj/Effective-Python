import asyncio
import aiohttp

import collections
import tqdm

from flag2_common import main, HTTPStatus, Result, save_flag

DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, contry_code):
        self.contry_code = contry_code


async def get_flag(session, base_url, cc):
    """最底层的协程函数, 异步下载一个文件.
    如果GET操作返回的状态是 200, 返回异步非阻塞式读取的结果;
    如果状态是404, 抛出 aiohttp.web.HTTPNotFound 异常;
    对于其他异常状态, 返回相应的 aiohttp.HttpProcessingError.
    """
    url = '{}/{cc}{cc}.gif'.format(base_url, cc=cc.lower())
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
        elif resp.status == 404:
            raise aiohttp.web.HTTPNotFound
        else:
            raise aiohttp.HttpProcessingError(
                          code=resp.status,
                          message=resp.version,
                          headers=resp.headers)


async def download_one(session, cc, base_url, semaphore, verbose):
    """委托生成器函数, 驱动 get_flag 协程函数
    """
    try:
        # semaphore 是一个 asyncio.Semaphore 的实例, 用来控制最大并发数
        # 因为它是 asyncio 的对象, 需要在前面 加 async
        # 等价于 with (yield from semaphore)
        async with semaphore:
            # 等价于 image = yield from get_flag(...)
            image = await get_flag(session, base_url, cc)
        # 退出上面的 with 语句时信号量减1, 使得某一个挂起的生成器函数重新运行
    # 下面的部分处理了 get_flag 抛出的异常:
    #  1.对于 aiohttp.web.HTTPNotFound, 吞掉它.
    #  2.其他异常用 FetchError 异常类封装后向上抛出
    except aiohttp.web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        # 注意这里的 raise X from Y 语法
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)


async def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    # 用信号量控制最大并发数
    semaphore = asyncio.Semaphore(concur_req)
    async with aiohttp.ClientSession() as session:
        # 创建 to_do list, list 中的每一个元素是一个生成器函数
        to_do = [download_one(session, cc, base_url, semaphore, verbose)\
                 for cc in sorted(cc_list)]
        # 获得一个生成器函数, 每当有一个协程完成就返回一个future对象
        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        # 在 to_do_iter 已经完成的部分(它们都返回一个 future 对象)上迭代
        for future in to_do_iter:
            try:
                # 等价于 res = yield from future
                # 注意, 不要调用 future.result()
                res = await future
            # download_one 函数抛出的所有异常都是 FetchError 的实例
            except FetchError as exc:
                country_code = exc.contry_code
                try:
                    # 试图从原始异常中获取错误信息(注意我们用了 yield X from Y 语法, 这里获取 Y 的错误信息)
                    error_msg = exc.__cause__.args[0]
                except IndexError:
                    # 如果我们没能获得原是错误信息, 就用原始原始异常的名字作为错误信息
                    error_msg = exc.__caluse__.__class__.__name__
                if verbose and error_msg:
                    msg = '*** Error for {}: {}'
                    print(msg.format(country_code, error_msg))
                status = HTTPStatus.error
            else:
                status = res.status
            counter[status] += 1
        return counter


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

