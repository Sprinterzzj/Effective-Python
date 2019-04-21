#!/usr/bin/env python
# coding: utf-8

# In[2]:


#我们首先来看看 decorator 解决哪些问题


# In[3]:


def add(x, y=10):
    return x + y


# In[4]:


add(10, 20)


# ### 检查add函数

# In[5]:


add


# In[6]:


add.__name__


# In[7]:


add.__module__


# In[8]:


add.__defaults__


# In[9]:


add.__code__.co_varnames


# In[11]:


#你甚至可以查看 add的源代码
from inspect import getsource
print(getsource(add))


# In[12]:


#add函数执行加法运算。
#现在你需要在add函数中执行“额外的功能”，比如timing


# In[13]:


from time import time
def add(x, y=10):
    before = time()
    rv = x + y
    after = time()
    print('Time taken: ', after - before)
    return rv


# In[15]:


print('add(10):', add(10))


# In[17]:


#但是上面的办法不具有普遍性: 如果你有其他的执行二元运算的函数也想timing，
#你需要一个一个改写他们！！！
#一个进阶的办法是用warp函数


# In[18]:


def timer(func):
    def f(x, y=10):
        before = time()
        rv = func(x, y)
        after = time()
        print('Time Taken: ', after - before)
        return rv
    return f


# In[20]:


def add(x, y=10):
    return x + y
add = timer(add)
add(3, 5)


# In[21]:


#Decorator 简化了上面的写法


# In[22]:


@timer
def add(x, y=10):
    return x + y


# In[24]:


add(3, 5)


# In[25]:


#一般情况下 decorator用来在函数调用之前和之后执行一些额外的操作


# In[26]:


def time(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print('Time taken: ', after - before)
        return rv
    return f


# In[27]:


#当然你也可以搞更高阶的decorator 但通常情况没有必要


# In[28]:


def ntimes(n):
    def inner(f):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                rv = f(*args, **kwargs)
            return rv
        return wrapper
    return inner


# ### 摘自 scipy笔记

# #### 装饰器函数

# In[40]:


#简单装饰器, 返回原来的函数
def simple_decorator(func):
    print('Doing decoration')
    return func

#装饰器在定义函数的时候就
#已经执行了, 因此可以被用来
#在内部函数执行前后做一些
#额外的工作
@simple_decorator
def func():
    print('Inside function.')


# In[41]:


func()


# In[44]:


#带参数的装饰器, 返回原来的函数
def decorator_with_args(arg):
    print('defining the decorator.')
    def _decorator(func):
        #内部函数中 args仍然可见
        print('doing decoration, %r' % arg)
        return func
    return _decorator


# In[45]:


@decorator_with_args('abc')
def func():
    print('Inside function.')


# In[47]:


#简单装饰器, 返回新的函数 _wrapper
def simple_decorator(func):
    print('Defining the decorator.')
    def _wrapper(*args, **kwargs):
        print("Inside wrapper, %r %r" % (args, kwargs))
        return func(*args, **kwargs)
    return _wrapper        


# In[50]:


@simple_decorator
def func(*args, **kwargs):
    print('Inside function, %r %r' % (args, kwargs))
    return 14


# In[51]:


func(1,2, a = 3)


# In[58]:


#带参数的装饰器, 返回新的函数 _wrapper
def decorator_with_args(arg):
    print('Defining the decorator.')
    def _decorator(func):
        print("Doing decoration, %r" % arg)
        def _wrapper(*args, **kwargs):
            print("Inside wrapper, %r %r" % (args, kwargs))
            return func(*args, **kwargs)
        print("Finish decoration, %r" % arg)
        return _wrapper
    print('Finish the decorator.')
    return _decorator


# In[59]:


@decorator_with_args('abc')
def func(*args, **kwargs):
    print('Inside function, %r %r' % (args, kwargs))
    return 14


# In[60]:


func(11, 12, a = 3)


# #### 装饰器类

# In[70]:


#返回原始函数的装饰器类
class decorator_class(object):
    def __init__(self, arg):
        print("In decorator init, %s"% arg)
        self.arg = arg
    def __call__(self, func):
        print('In decorator call, %s' % self.arg)
        return func


# In[67]:


deco_instance = decorator_class(arg = 'foo')


# In[68]:


@deco_instance
def function(*args, **kwargs):
    print('In function, %s %s' % (args, kwargs))


# In[69]:


function()


# #### 这段代码很重要

# In[72]:


#返回新的object的装饰器类
class replacing_decorator_class(object):
    def __init__(self, arg):
        print('In decorator init, %s' % arg)
        self.arg = arg
    def __call__(self, func):
        print('In decorator call, %s' % self.arg)
        self.func = func
        return self._wrapper
    def _wrapper(self, *args, **kwargs):
        print('In the wrapper, %s %s' % (args, kwargs))
        return self.func(*args, **kwargs)


# In[74]:


#初始化函数在类的实例化时运行
deco_instance = replacing_decorator_class(arg = 'foo')


# In[76]:


#__call__函数在装饰器装配时运行,
#同时初始化func成员
#然后返回wrapper, 一个新的对象。
@deco_instance
def func(*args, **kwargs):
    print('In function, %s %s' % (args, kwargs))


# In[78]:


#在wrapper方法中运行func
func(0,1, a = 3)


# In[ ]:




