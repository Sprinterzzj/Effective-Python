#!/usr/bin/env python
# coding: utf-8

# ##### 例子: Web Downloads

# In[22]:


import os
import time
import sys
import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

########################


def main(download_func):
    t0 = time.time()
    count = download_func(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


# ###### 顺序下载

# In[23]:


def download_sequentially(cc_list):
    res = []
    for cc in sorted(cc_list):
        res.append(download_one(cc))
    return len(res)


# In[24]:


main(download_sequentially)


# ###### 线程池下载

# In[26]:


from concurrent import futures
MAX_WORKERS = 20


def download_concurrently(cc_list):
    """该函数没有显式的调用Future
    """
    num_workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(num_workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))


# In[27]:


main(download_concurrently)


# ###### 显式地调用Furture对象的并发版本

# In[29]:


def download_concurrently_v2(cc_list):
    num_workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(num_workers) as executor:
        
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {} : {}'
            print(msg.format(cc, future))
        
        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result : {!r}'
            print(msg.format(future, res))
            results.append(res)
    
    return len(results)      


# In[30]:


main(download_concurrently_v2)


# <center>关于Python中的多线程</center>
# 
# Every blocking I/O function in the Python standard library **releases the GIL**, allowing other threads to run. <br>
# The time.sleep() function also releases the GIL. <br>
# Therefore, Python threads are per‐fectly usable in I/O-bound applications, despite the GIL.

# ##### Concurrent.futures 的若干功能

# ###### Executor.map

# In[4]:


from time import sleep, strftime
from concurrent import futures

def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10


# In[7]:


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=4)
    results = executor.map(loiter, range(8))
    display('result:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {} : {}'.format(i, result))


# In[8]:


main()


# <center> Executor.map 的特点</center>
# 
# 1. 它返回一个生成器对象, 里面**按调用的顺序储存了运行结果**. 因此如果前面的调用耗时比较长, 生成器一开始可能阻塞

# In[ ]:




