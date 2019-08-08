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
    try:
        async with semaphore:
            image = await get_flag(session, base_url, cc)
        except web.HTTPNotFound:
            status = HTTPStatus.not_found
            msg = 'not found'
        except Exception as exec:
            raise FetchError(cc) from exc
        else:
            save_flag(image, cc.lower() + '.gif')
            status = HTTPStatus.ok
            msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return Result(result, cc)

