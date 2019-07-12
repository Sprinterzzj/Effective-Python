#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#装饰器函数与装饰器类" data-toc-modified-id="装饰器函数与装饰器类-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>装饰器函数与装饰器类</a></span><ul class="toc-item"><li><span><a href="#装饰器函数" data-toc-modified-id="装饰器函数-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>装饰器函数</a></span></li><li><span><a href="#装饰器类" data-toc-modified-id="装饰器类-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>装饰器类</a></span></li></ul></li><li><span><a href="#使用装饰器的例子" data-toc-modified-id="使用装饰器的例子-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>使用装饰器的例子</a></span><ul class="toc-item"><li><span><a href="#classmethod" data-toc-modified-id="classmethod-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>classmethod</a></span></li><li><span><a href="#staticmethod" data-toc-modified-id="staticmethod-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>staticmethod</a></span></li><li><span><a href="#property" data-toc-modified-id="property-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>property</a></span></li><li><span><a href="#deprecation-of-function" data-toc-modified-id="deprecation-of-function-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>deprecation of function</a></span></li><li><span><a href="#WHILE-loop-removing-decorator" data-toc-modified-id="WHILE-loop-removing-decorator-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>WHILE-loop removing decorator</a></span></li><li><span><a href="#plugin-registration-system" data-toc-modified-id="plugin-registration-system-2.6"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>plugin registration system</a></span></li><li><span><a href="#不使用-@wraps来保持原始函数的信息" data-toc-modified-id="不使用-@wraps来保持原始函数的信息-2.7"><span class="toc-item-num">2.7&nbsp;&nbsp;</span>不使用 @wraps来保持原始函数的信息</a></span></li><li><span><a href="#利用装饰器定义属性" data-toc-modified-id="利用装饰器定义属性-2.8"><span class="toc-item-num">2.8&nbsp;&nbsp;</span>利用装饰器定义属性</a></span></li></ul></li></ul></div>

# ##### 装饰器函数与装饰器类
# ###### 装饰器函数

# 简单装饰器, 返回原来的函数

# In[2]:


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


# 带参数的装饰器, 返回原来的函数

# In[3]:


def decorator_with_args(arg):
    print('defining the decorator.')
    def _decorator(func):
        #内部函数中 args仍然可见
        print('doing decoration, %r' % arg)
        return func
    return _decorator

@decorator_with_args('abc')
def func():
    print('Inside function.')


# 简单装饰器, 返回新的函数 _wrapper

# In[47]:



def simple_decorator(func):
    print('Defining the decorator.')
    def _wrapper(*args, **kwargs):
        print("Inside wrapper, %r %r" % (args, kwargs))
        return func(*args, **kwargs)
    return _wrapper        

@simple_decorator
def func(*args, **kwargs):
    print('Inside function, %r %r' % (args, kwargs))
    return 14


# 带参数的装饰器, 返回新的函数 \_wrapper

# In[4]:


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

@decorator_with_args('abc')
def func(*args, **kwargs):
    print('Inside function, %r %r' % (args, kwargs))
    return 14


# ###### 装饰器类

# 返回原始函数的装饰器类

# In[5]:


class decorator_class(object):
    def __init__(self, arg):
        print("In decorator init, %s"% arg)
        self.arg = arg
    def __call__(self, func):
        print('In decorator call, %s' % self.arg)
        return func

deco_instance = decorator_class(arg = 'foo')
@deco_instance
def function(*args, **kwargs):
    print('In function, %s %s' % (args, kwargs))


# **返回新对象的装饰器类**

# In[8]:


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

#初始化函数在类的实例化时运行
deco_instance = replacing_decorator_class(arg = 'foo')

#__call__函数在装饰器装配时运行,
#同时初始化func成员
#然后返回wrapper, 一个新的对象。
@deco_instance
def func(*args, **kwargs):
    print('In function, %s %s' % (args, kwargs))

#在wrapper方法中运行func
func(0,1, a = 3)


# 注意上面的 replacing_decorator_class 会返回 \_wrapper成员.<br>
# 这么做的一个弊端是: 原始函数 func的名字, doc, 参数列表全部丢失.<br>
# **解决方案: functools.update_wrapper 或 functools.wraps**

# In[14]:


from functools import update_wrapper, wraps
#functools.update_wrapper
def replacing_decorator_with_args(arg):
    print('defining the decorator')
    def _decorator(function):
        print('doing decoration, %r' % arg)
        def _wrapper(*args, **kwargs):
            print('inside wrapper, %r %r' % (args, kwargs))
            return function(*args, **kwargs)
        return update_wrapper(_wrapper, function)
    return  _decorator

@replacing_decorator_with_args('abc')
def function(a = 13):
    """
    extensive documentation
    """
    print('inside function')
    return 14

#原始函数的名字和doc都可以拷贝过来
print(function.__name__, function.__doc__)

#但是参数列表依然无法copy
function.__code__.co_varnames


# In[16]:


#functools.wraps
def replacing_decorator_with_args(arg):
    print('defining the decorator')
    def _decorator(function):
        print('doing decoration, %r' % arg)
        @wraps(function)
        def _wrapper(*args, **kwargs):
            print('inside wrapper, %r %r' % (args, kwargs))
            return function(*args, **kwargs)
        return _wrapper
    return  _decorator

@replacing_decorator_with_args('abc')
def function(a = 13):
    """
    extensive documentation
    """
    print('inside function')
    return 14

#原始函数的名字和doc都可以拷贝过来
print(function.__name__, function.__doc__)

#同上, 参数列表无法被copy
function.__code__.co_varnames


# ##### 使用装饰器的例子

# ###### classmethod

# In[17]:


import numpy as np
class Array(object):
    def __init__(self, data):
        self.data = data
    
    #classmethod作为工厂方法, 创建类的实例
    @classmethod
    def fromfile(cls, file):
        data = np.load(file)
        return cls(data)


# ###### staticmethod

# In[23]:


#在开发中，我们常常需要定义一些方法，这些方法跟类有关，但在实现时并不需要引用类或者实例，
#例如，设置环境变量，修改另一个类的变量，等。这个时候，我们可以使用静态方法。 


# ###### property

# 注意只实现了property的属性是 read-only的

# In[21]:


class A(object):
    @property
    def a(self):
        """an important attribute
        """
        return 'a value'

print(A().a)

try:
    A().a = 3
except AttributeError:
    print('没有实现setter方法.')


# 你可以实现setter方法, 让它可以被赋值

# In[22]:


class Rectangle(object):
    def __init__(self, edge):
        self.edge = edge
    @property
    def area(self):
        return self.edge **2
    @area.setter
    def area(self, area):
        self.edge = area ** .5


# ###### deprecation of function

# In[29]:


#我们要在某个函数第一次调用时打出 deprecation警告
class deprecated(object):
    def __call__(self, func):
        self.func = func
        self.count = 0
        return self._wrapper
    def _wrapper(self, *args, **kwrags):
        self.count += 1
        if self.count == 1:
            print(self.func.__name__, 'is deprecated')
        return self.func(*args, **kwargs)    

#你也可以用装饰器函数
def deprecated(func):
    count = [0]
    def wrapper(*args, **kwargs):
        count[0] += 1
        if count[0] == 1:
            print(func.__name__, 'is deprecated')
        return func(*args, **kwargs)
    return wrapper


# ######  WHILE-loop removing decorator

# In[23]:


#当然你也可以直接用 yield, 但是某些情况下 list(EXPR) 会比较丑
def vectorized(gen_func):
    """
    Parameters
    ----------
    gen_func: 生成器函数
    """
    def wrapper(*args, **kwargs):
        return list(gen_func(*args, **kwargs))
    return update_wrapper(wrapper, gen_func)

@vectorized
def find_answers():
    while True:
        ans = look_for_next_answer()
        if ans is None:
            break
        yield ans


# ###### plugin registration system

# In[ ]:


#WordProcessor装饰器类不会更改他装饰的类, 而是把他加到PLUGINS中去
class WordProcessor(object):
    PLUGINS = []
    #process方法实例化PLUGINS中的类,然后执行他们
    def process(self, text):
        for plugin in self.PLUGINS:
            text = plugin().cleanup(text)
        return text
    @classmethod
    def plugin(cls, plugin):
        cls.PLUGINS.append(plugin)

@WordProcessor.plugin
class CleanMdashesExtension(object):
    def cleanup(self, text):
        return text.replace('&mdash', u'\N{em dash}')


# ###### 不使用 @wraps来保持原始函数的信息

# In[41]:


def simple_decorator(decorator):
    """
    你的装饰器函数 `decorator`必须足够简单:
    1. 接受一个函数, 返回一个函数
    2. 不修改函数的属性和文档
    """
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # 下面要修改 new_decorator, 使得它和原装饰器函数一致
    # print(new_decorator.__name__)
    new_decorator.__name__ = decorator.__name__
    # print(new_decorator.__name__)
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

def demo_logging_decorator(func):
    def wrapper(*args, **kwargs):
        print('calling {}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def better_demo_logging_decorator(func):
    def wrapper(*args, **kwargs):
        print('calling {}'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper

def add(x, y):
    '两数相加'
    return x + y

@demo_logging_decorator
def add_with_log(x, y):
    '两数相加'
    return x + y

@better_demo_logging_decorator
def add_with_log_v2(x, y):
    '两数相加'
    return x + y


print('装饰之前:')
print(add.__name__)
print(add.__doc__)
print(add.__dict__)
print('使用了 demo_logging_decorator:')
print(add_with_log.__name__)
print(add_with_log.__doc__)
print(add_with_log.__dict__)
print('使用了 better_demo_logging_decorator:')
print(add_with_log_v2.__name__)
print(add_with_log_v2.__doc__)
print(add_with_log_v2.__dict__)


# ###### 利用装饰器定义属性

# In[64]:


import sys
def test(a, b):
    #获取当前函数的局部变量
    print(sys._getframe(0).f_locals)
    #获取main的全部变量, 这里面包括:
    #1. 导入的模块
    #2. 用户定义的函数(def)
    print(sys._getframe(1).f_locals.keys())


# In[65]:


test(2, 3)


# In[ ]:




