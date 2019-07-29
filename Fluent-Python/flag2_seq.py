"""Download flags of countries with error handling.
"""


import collections

import requests
import tqdm

from flag2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

# BEGIN FLAGS2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200: #1 如果 status_code 不是 200, 就用 raise_for_status 向外抛出异常
        resp.raise_for_status()
    return resp.content


#注意通过base_url和cc来获得下载页面
def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    except requests.exceptions.HTTPError as exc: #2 捕捉HTTPError异常, 并且对404做特殊处理(status_code是404的异常不会被抛出)
        res = exc.response
        if res.status_code == 404:
            status = HTTPStatus.not_found  #3
            msg = 'not found'
        else: #4 其他异常向外抛出
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose:
        print(cc, msg)
    return Result(status, cc) # 注意返回的数据结构, 值得借鉴!
# END FLAGS2_BASIC_HTTP_FUNCTIONS

# BEGIN FLAGS2_DOWNLOAD_MANY_SEQ
def download_many(cc_list, base_url, verbose, max_req):
    counter = collections.Counter() #1 对download的结果做统计: ok, not_found 和 error
    cc_iter = sorted(cc_list) #2 
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter) #3
    for cc in cc_iter: #4 主循环
        try:
            res = download_one(cc, base_url, verbose) #5 
        except requests.exceptions.HTTPError as exc: #6 HTTP相关的error, 这些error由 get_flag抛出并且没有被donwload_one处理的, 会在这里处理.
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        except requests.exceptions.ConnectionError as exc: #7 其他网络相关的异常在这里处理, 非网络相关的异常会终止脚本运行
            error_msg = 'Connection error'
        else: #8 如果没有异常就接受 download_one 函数返回的状态
            error_msg = ''
            status = res.status
        
        if error_msg:
            status = HTTPStatus.error #9 
        counter[status] +=1 #10 统计返回的状态
        if verbose and error_msg: #11
            print('*** Error for {}:{}'.format(cc, error_msg))
    return counter #12
# END FLAGS2_DOWNLOAD_MANY_SEQ

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)