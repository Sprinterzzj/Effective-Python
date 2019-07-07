#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#协程及其执行过程" data-toc-modified-id="协程及其执行过程-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>协程及其执行过程</a></span><ul class="toc-item"><li><span><a href="#例子:-用协程实现-Running-Average" data-toc-modified-id="例子:-用协程实现-Running-Average-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>例子: 用协程实现 Running Average</a></span></li><li><span><a href="#用装饰器激活协程函数" data-toc-modified-id="用装饰器激活协程函数-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>用装饰器激活协程函数</a></span></li><li><span><a href="#协程的异常处理" data-toc-modified-id="协程的异常处理-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>协程的异常处理</a></span></li><li><span><a href="#协程的返回值" data-toc-modified-id="协程的返回值-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>协程的返回值</a></span></li></ul></li><li><span><a href="#yield-from" data-toc-modified-id="yield-from-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>yield from</a></span><ul class="toc-item"><li><span><a href="#yield-from-的使用" data-toc-modified-id="yield-from-的使用-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>yield from 的使用</a></span></li></ul></li><li><span><a href="#yield-from-的含义" data-toc-modified-id="yield-from-的含义-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>yield from 的含义</a></span><ul class="toc-item"><li><span><a href="#一个简化的情形" data-toc-modified-id="一个简化的情形-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>一个简化的情形</a></span></li><li><span><a href="#较为真实的情形" data-toc-modified-id="较为真实的情形-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>较为真实的情形</a></span></li></ul></li><li><span><a href="#Use-Case:-离散事件模拟---出租车模拟" data-toc-modified-id="Use-Case:-离散事件模拟---出租车模拟-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Use Case: 离散事件模拟-- 出租车模拟</a></span></li></ul></div>

# ##### 协程及其执行过程

# 在生成器协程中:
# 
# ```python
# SEND = yield RECEIVE
# ```
# 
# 它就成了协程.
# 注意:
# 
# 1. The value of `SEND` will only be set when the coroutine is activated later by the client code.
# 2. 协程退出时会抛出StopIteration异常

# In[3]:


def simple_coroutine():
    print('开始协程')
    x = yield 3
    print('协程中止')


my_cro = simple_coroutine()
#激活生成函数, 函数运行到 `x = yield 3` 处阻塞
my_cro.send(None)
#给生成器发送值到x, 并且接受 生成器 yield的值
try:
    print('从协程中得到, ', my_cro.send(42))
except StopIteration as e:
    pass


# <center>协程的执行过程</center>
#     
# ![协程流程](img/16_1.png)

# In[12]:


def simple_coro2(a):
    print('协程开始: a=', a)
    b = yield a
    print('协程接受: b=', b)
    c = yield a + b
    print('协程接受: c=', c)


my_coro2 = simple_coro2(14)

print('协程返回', my_coro2.send(None))

print('协程返回', my_coro2.send(28))

try:
    my_coro2.send(99)
except StopIteration as e:
    pass


# ###### 例子: 用协程实现 Running Average

# In[19]:


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        try:
            term = yield average
        except GeneratorExit:
            break
        else:
            total += term
            count += 1
            average = total/count


# In[20]:


coro_avg = averager()
item_list = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i, item in enumerate(item_list):
    print(f'第{i+1}次协程的返回值: {coro_avg.send(item)}')
print(f'协程关闭时的返回值: {coro_avg.close()}')


# ###### 用装饰器激活协程函数
# 用装饰器完成协程的激活

# In[21]:


from functools import wraps

def coroutine(func):
    """自己实现的装饰器函数, 完成协程函数的激活
    """
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return primer


# ###### 协程的异常处理
# 
# ```python
# generator.throw(exc_type[, exc_value[, traceback]])
# ```
# 在协程函数挂起的yield表达式处抛出相应的异常.
# 
# 1. 如果生成器处理了这个异常, 那么执行流推进到下一个yield语句中, 且yield生成的值就作为generator.throw的返回值
# 2. 如果生成器没有处理异常, 异常向上冒泡, 生成器关闭
# 
# ```python
# generator.close()
# ```
# 在协程函数挂起的yield表达式处抛出**GeneratorExit**异常.
# 
# 1. 如果生成器不处理**GeneratorExit**异常, 那么该异常不会报告给调用者
# 2. 如果生成器显式的处理了上述的异常, 那么生成器必须不再yield value, 否则会抛出RuntimeError异常. 生成器的任何其他异常都会冒泡给调用者

# In[34]:


class DemoException(Exception):
    pass

def demo_exc_handling():
    print('协程开始')
    x = yield 
    print('接收到: ', x)
    try:
        ## print('如果没有发生异常, 生成的值为:\n')
        y = yield x
    except DemoException:
        print('如果没有发生异常, 生成的值为: {0}\n'
              '如果发生了异常, 生成的值为:\n'.format(x))   
    yield (x + 1)
    z = yield x


exc_coro = demo_exc_handling()

exc_coro.send(None)

exc_coro.send(233)

exc_coro.throw(DemoException)


# ###### 协程的返回值
# 
# 1. 为了得到协程函数返回值, 我们不能调用它的close方法; 需要传递一个自己定义好的终止符作为循环终止的flag.
# 2. 协程的返回值放在**StopIteration**的value属性里(协程正常退出时一定会抛出StopIteration异常给调用方).

# In[38]:


GEN_END = 'end'
def averager_with_return():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average   
        #加入生成器终止的条件
        if term == GEN_END:
            return (count, average)        
        total += term
        count += 1
        average = total / count               


# In[40]:


coro_avg = averager_with_return()
item_list = [None, 1, 2, 3, 4, 5, GEN_END]
for i, item in enumerate(item_list):
    try:
        print(f'第{i+1}次协程的返回值: {coro_avg.send(item)}')
    except StopIteration as e:
        print(f'协程关闭时的返回值: {e.value}')


# ##### yield from

# In[43]:


#yield 和 yield from的区别
def gen():
    yield range(1, 3)
    yield from range(1, 3)

print(list(gen()))


# 我们可以用 yield from 来模拟 chain 方法:

# In[1]:


def cahin(*iterables):
    for it in iterables:
        yield from it


# ###### yield from 的使用
# 一些概念:
# 
# 1. 委托生成器: 包含了
# ```python 
# yield from <iterable>```
# 语句的生成器函数
# 2. 子生成器函数: 上面语句右边的生成器函数
# 3. 调用者: 调用委托生成器的函数
# 
# 来看下面的例子:

# In[3]:


from collections import namedtuple
Result = namedtuple('Result', 'count average')

#子生成器函数, 统计货物的数目并计算均值
def averager():
    total = 0.0
    count = 0.0
    average = None
    while True:
        term  = yield
        #循环终止的条件
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)

#委托生成器函数
def grouper(results, key):
    """当send给 grouper值时, 它将值传递给子生成器然后挂起,
    该值对grouper是不可见的.
    """
    while True:
        results[key] = yield from averager()

#客户端函数, 也就是调用者
def main(data):
    results = {}
    for key, values in data.items():
        #创建委托生成器
        #上一次循环中的委托生成器以及子生成器都被回收
        group = grouper(results, key)
        #激活子生成器
        group.send(None)
        for value in values:
            group.send(value)
        #重要: 终止子生成器, 子生成器抛出StopIteration异常, 
        #子生成器的返回值是该异常的第一个参数, yield from
        #自动处理异常并且把返回值赋值给 yield from 等号左边
        group.send(None)
    print(results)


# In[6]:


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))

data = {
    'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],     
    'girls;m':  [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],     
    'boys;kg':  [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],     
    'boys;m':   [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}

main(data)


# <center>上面的协程函数总结如下:</center>
# 
# ![示例](img/16_2.png)

# ##### yield from 的含义 
# ```python
# RESULT = yield from EXPR
# ```
# 
# <center> yield from 内部做了以下4件事:</center>
# 
# 1. 子生成器 yield 的任何值都被直接传送给调用委托生成器的函数, 也就是调用者
# 2. 调用委托生成器send 方法传送给委托生成器的任何值都被直接发送给子生成器:
#         2.1 如果发送的值是None, 那么调用子生成器的next方法
#         2.2 如果发送的值不是None, 那么调用子生成器的send方法
#         2.3 如果调用子生成器的 send方法抛出了 StopIteration异常, 那么委托生成器结束挂起.
#         2.4 任何其他异常都会范递给委托生成器
# 3. 在生成器中的 return expr 语句会抛出 StopIteration(expr) 异常
# 4. 由 3, yield from 的返回值是 StopIteration 的第一个参数
# 
# <center> yield from 还需要做关于异常处理的事 </center>
# 
# 1. 如果 GeneratorExit 抛入到委托生成器中, 或者调用了委托生成器的 close 方法;那么如果子生成器有 close方法, 就调用子生成器的close方法. 如果调用子生成器的close方法抛出了异常, 异常传递给委托生成器; 如果没有抛出异常, 那么在委托生成器中抛出 GeneratorExit.
# 2. 如果其他异常被抛给委托生成器, 那么调用子生成器的 throw 方法将异常抛给子生成器. 如果调用用子生成器的 throw 方法抛出了StopIteration异常, 那么委托生成器结束挂起; 如果抛出了其他异常, 那么异常传递给委托生成器.

# ###### 一个简化的情形
# **首先做几点假设**:
# 1. 调用方不会调用委托生成器的 throw 和 close 方法
# 2. 子生成器顺利运行直到抛出 StopIteration 异常
# 
# 下面的伪代码 与 
# ```python
# RESULT = yield from EXPR
# ```
# 等效.
# ```python
# _i = iter(EXPR) #1
# try:
#     _y = next(_i) #2
# except StopIteration as _e:
#     _r = _e.value #3
# else:
#     while 1: #4
#         _s = yield _y #5
#         try:
#             _y = _i.send(_s) #6
#         except StopIteration as _e: #7
#             _r = _e.value
#             break
# RESULT = _r #8
# ```
# 
# 下面逐行解释:
# 
# 1. EXPR 只需是 **可迭代的对象**, 而不必须是一个生成器, 因而调用 iter 方法得到一个迭代器 \_i, 也就是子生成器.
# 2. 激活子生成器, 并且取得子生成器的第一个值
# 3. 如果激活子生成器时抛出了StopIteration异常, 那么从异常中取出结果
# 4. 只要进入这一个While 循环, **委托生成器就挂起**, 这时委托生成器只是**调用者和子生成器之间的通道**
# 5. 子生成器 yield \_y 给 委托生成器; 调用者 send \_s 给委托生成器
# 6. 委托生成器尝试 调用子生成器的 send 方法, 把 \_s 传送过去; 并且接受 子生成器的下一个值 \_y
# 7. 如果调用 子生成器的 send 方法时 抛出 StopIteration 异常, 就获得异常的第一个参数, 赋值给 \_r, 然后中断循环, **委托生成器结束挂起**
# 8. \_r 的值赋值给 RESULT.
# 

# ###### 较为真实的情形

# 实际中, 我们需要处理以下情形:
# 
# 1. 调用者可能调用 委托生成器的 close 和 throw 方法. 如果 子生成器没有 close 和 throw 方法(只是迭代器), 那么需要相应的处理; 如果子生成器支持 close 和 throw 方法, 那么需要再合适的地方 调用他们.
# 2. 子生成器可能抛出自己的异常.
# 3. 只有调用者调用 send 方法 传递 非None 值的时候才会调用子生成器的 send 方法
# 
# 这样伪代码变得更加复杂:
# ```python
# _i = iter(EXPR) #1
# try:
#     _y = next(_i) #2
# except StopIteration as _e:
#     _r = _e.value #3
# else:
#     while 1: #4
#         try:
#             _s = yield _y #5
#         except GeneratorExit as _e: #6
#             try:
#                 _m = _i.close
#             except AttributeError:
#                 pass
#             else:
#                 _m()
#             raise _e
#         except BaseException as _e: #7
#             _x = sys.exc_info()
#             try:
#                 _m = _i.throw
#             except AttributeError:
#                 raise _e
#             else: #8
#                 try:
#                     _y = _m(*_x)
#                 except StopIteration as _e:
#                     _r = _e.value
#                     break
#         else: #9
#             try: #10
#                 if _s is None: #11
#                     _y = next(_i)
#                 else:
#                     _y = _i.send(_s)
#             except StopIteration as _e: #12
#                 _r = _e.value
#                 break
# RESULT = _r #13
# ```
# 
# 逐行解释:
# 
# 6. 调用者调用了委托生成器的close方法, 试子生成器有无close 方法分情况处理:
#         6.1 如果有 close方法, 就调用子生成器的close 方法
#         6.2 如果没有 close 方法, 在委托生成器中抛出异常 
# 7. 调用者调用了委托生成器的 throw 方法, 同样子生成器可以没有 throw 方法.
# 8. 如果子生成器有 throw 方法, 把来自调用者的异常传递给他, 此时:
#         8.1 子生成器处理了异常, 循环继续
#         8.2 子生成器抛出了 StopIteration 异常, 循环终止
#         8.3 子生成器也可能抛出除了 StopIteration 之外的异常, 那么异常抛给委托生成器
# 9. 没有任何异常就开始 yield
# 11. 如果调用者传递的值是None, 就调用子生成器的 next 方法.
#       

# ##### Use Case: 离散事件模拟-- 出租车模拟

# In[14]:


from collections import namedtuple
Event = namedtuple('Event', ['time', 'proc', 'action'])


# In[15]:


def taxi_process(ident, trips, start_time=0):
    """
    模拟拟出租车运行的生成器函数
    
    Parameters
    ----------
    ident: 出租车 id
    trips: 出租车每个工作日要完成的载客数
    start_time: 出租车开始运行的时间
    """
    time = yield Event(start_time, ident, '离开车站')
    for i in range(trips):
        time = yield Event(time, ident, '乘客上车')
        time = yield Event(time, ident, '乘客下车')
    yield Event(time, ident, '下班回家')
    return


# In[29]:


#使用
from time import time 

taxi = taxi_process(ident=13, trips=2, start_time=0)
print(taxi.send(None))

print(taxi.send(time() + 7))
print(taxi.send(time() + 23))
print(taxi.send(time() + 7))
print(taxi.send(time() + 23))
print(taxi.send(time() + 10))

#最后生成器抛出异常
try:
    taxi.send(time() + 10)
except StopIteration:
    print('生成器终止')


# In[ ]:




