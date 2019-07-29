import collections
from concurrent import futures

import requests
import tqdm #1

from flag2_common import main, HTTPStatus #2
from flag2_seq import download_one #3

DEFAULT_CONCUR_REQ = 30 #4
MAX_CONCUR_REQ = 1000 #5


def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor: #6
        to_do_map = {} #7 键: future对象, 代表了一个下载的线程; 值: 国旗代码
        for cc in sorted(cc_list): #8
            future = executor.submit(download_one, cc, base_url, verbose) #9 提交任务, 立刻返回future对象
            to_do_map[future] = cc #10 
        done_iter = futures.as_completed(to_do_map) #11 as_completed returns an iterator that yields futures as they are done
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list)) #12 注意这里的total参数设置
        for future in done_iter: #13 Iterate over the futures as they are completed
            try:
                res = future.result()  # <14> 当你调用result方法时, 或者返回正常的返回值, 或者抛出任何线程的函数抛出的异常
            except requests.exceptions.HTTPError as exc:  # <15> 所以你需要用 try exp 来接受抛出的异常
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status
                
            if error_msg:
                status = HTTPStatus.error
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future] #16
                print('*** Error for {}: {}'.format(cc, error_msg))
    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
