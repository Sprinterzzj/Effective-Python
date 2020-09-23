#!/usr/bin/env python
# coding: utf-8

# ### functool.wraps 模块

# In[2]:


#定义函数装饰器
#装饰器可以在被warp的函数call之前/之后，运行额外的代码
#比如说,你想打印调用的函数名以及函数的返回值

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        #func.__name__获取函数名字
        print('%s(%r, %r) -> %r' %              (func.__name__, args, kwargs, result))
        return result
    return wrapper


# In[4]:


#用 @symbol来使用装饰器
#等价于 fibonacci = trace(fibonacci)
@trace
def fibonacci(n):
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


# In[5]:


fibonacci(3)


# In[6]:


#上面的用法有一个副作用，就是 装饰了trace的函数fibonacci,
#他的函数名不叫fibonacci:
print(fibonacci)
#这可以会给 debug和序列化 带来困难


# In[7]:


fibonacci.__name__


# In[8]:


#help函数也失效了
help(fibonacci)


# In[10]:


#解决方案: functools
from functools import wraps
def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %             (func.__name__, args, kwargs, result))
        return result
    return wrapper
            


# In[11]:


@trace
def fibonacci(n):
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


# In[12]:


help(fibonacci)


# In[13]:


fibonacci.__name__


# ### contextlib.contextmanager模块和with关键字

# In[16]:


#下面两个代码块是等价的
#使用 with的代码块更加简洁
from threading import Lock
lock = Lock()
with lock:
    print('Lock is held')

lock = Lock()
lock.acquire()
try:
    print('Lock is held')
finally:
    lock.release()


# In[18]:


#使用contexlib模块中的contextmanager可以
#是你的函数与 with联用
from contextlib import contextmanager


# In[25]:


#假设你想要你的程序打印一些log
import logging
def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')


# In[26]:


#默认的log level是WARNING,因此只会打印出error信息
my_function()


# In[27]:


#我可以定义如下的helper_function，通过with语句，他可以暂时修改log level
@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        #这是关键。在with里面捕捉到的任何异常都会传递到helper里
        yield
    finally:
        logger.setLevel(old_level)


# In[28]:


with debug_logging(logging.DEBUG):
    print('Inside: ')
    my_function()
print('After: ')
my_function()


# In[31]:


#用 as 来 管理 with返回的object
#例如
with open('my_text.txt', 'w') as handle:
    handle.write('This is some data')
#文件会在with语句结束后自动关闭。


# In[32]:


#我们可以更改我们的helper函数使它返回一个可以被 as 用的值
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)


# In[34]:


with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug('This is my message!')
    logging.debug('This will not print') #logging的默认等级是warning, 所以不会打印
#在with语句结束后,’my-log‘ logger不会打印出 debug log,因为log level 已经回到默认等级
logger = logging.getLogger('my-log')
logger.debug('Debug will not print')
logger.error('Error will print')


# ### datatime 模块

# In[56]:


#datetime模块要比time模块好用


# ### Built-in Algorithms & Data Structures

# In[57]:


#1. Double-ended Queue
from collections import deque
#常数时间内插入和删除元素
fifo = deque()
fifo.append(1) #Producer
x = fifo.popleft() #Consumer


# In[69]:


#2. Ordered Dictionary
#默认的字典是无序的。
#OrderedDict 保持了**value**插入的顺序:
from collections import OrderedDict
a = OrderedDict()
a['foo'] = 1
a['bar'] = 2
b = OrderedDict()
b['bar'] = 'red'
b['foo'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)


# In[70]:


#3. Default Dictionary
#默认的字典的一个问题是,你不能假设 一个 key是已经存在的
#defaultdict会在key不存在时引入默认的value
from collections import defaultdict
stats = defaultdict(int)
stats['my_counter'] += 1


# In[71]:


stats


# In[74]:


#4. Heap Queue
#维持一个优先队列
from heapq import heappush, heappop, nsmallest, nlargest
a = []
#插入元素按任意顺序在a里排列,但最小值一定在对列头部
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)


# In[75]:


a


# In[76]:


#但是删除元素是按照最高优先级(最小元素)删除
print(heappop(a), heappop(a), heappop(a), heappop(a))


# In[77]:


#头部元素一定是优先级最高的元素(最小元素)
a = [] 
heappush(a, 5) 
heappush(a, 3) 
heappush(a, 7) 
heappush(a, 4) 
assert a[0] == nsmallest(1, a)[0] == 3


# In[78]:


#排序不改变头号元素
print('Before: ', a)
a.sort()
print('After:, ', a)


# In[79]:


#4. Bisection
#用来做对数线性时间查找
x = list(range(10**6))
get_ipython().run_line_magic('time', 'i = x.index(991234)')


# In[80]:


from bisect import bisect_left
get_ipython().run_line_magic('time', 'i = bisect_left(x, 991234)')


# In[81]:


#5. Iterator tools
#itertools 模块含有三类:
##1. 链接两个迭代器:
#### chain 将复数个迭代器拼接起来
#### cycle 永远重复一个迭代器
#### tee 讲一个迭代器分割成数个平行的迭代器
#### zip_longest zip built-in模块的变种,处理两个迭代器长度不等的情形
##2. 过滤一个迭代器:
#### islice 切片一个迭代器,不返回拷贝
#### takewhile, dropwhile
#### filterfalse 当func返回 False时,return 这些元素。这与 filter built-in模块作用相反。
##3. 将复数个迭代器的元素结合起来
#### product 返回 一个迭代器的 Cartesian 乘积, 可以用来做 deep nested list comprehensions
#### permutation  返回长度为N的排列
#### combination 返回长度为N的无重复组合


# In[ ]:




