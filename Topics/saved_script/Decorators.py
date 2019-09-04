#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#装饰器函数与装饰器类" data-toc-modified-id="装饰器函数与装饰器类-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>装饰器函数与装饰器类</a></span><ul class="toc-item"><li><span><a href="#装饰器函数" data-toc-modified-id="装饰器函数-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>装饰器函数</a></span></li><li><span><a href="#装饰器类" data-toc-modified-id="装饰器类-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>装饰器类</a></span></li></ul></li><li><span><a href="#使用装饰器的例子" data-toc-modified-id="使用装饰器的例子-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>使用装饰器的例子</a></span><ul class="toc-item"><li><span><a href="#classmethod" data-toc-modified-id="classmethod-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>classmethod</a></span></li><li><span><a href="#staticmethod" data-toc-modified-id="staticmethod-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>staticmethod</a></span></li><li><span><a href="#property" data-toc-modified-id="property-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>property</a></span></li><li><span><a href="#deprecation-of-function" data-toc-modified-id="deprecation-of-function-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>deprecation of function</a></span></li><li><span><a href="#WHILE-loop-removing-decorator" data-toc-modified-id="WHILE-loop-removing-decorator-2.5"><span class="toc-item-num">2.5&nbsp;&nbsp;</span>WHILE-loop removing decorator</a></span></li><li><span><a href="#plugin-registration-system" data-toc-modified-id="plugin-registration-system-2.6"><span class="toc-item-num">2.6&nbsp;&nbsp;</span>plugin registration system</a></span></li></ul></li><li><span><a href="#摘自-https://wiki.python.org/moin/PythonDecoratorLibrary" data-toc-modified-id="摘自-https://wiki.python.org/moin/PythonDecoratorLibrary-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>摘自 <a href="https://wiki.python.org/moin/PythonDecoratorLibrary" target="_blank">https://wiki.python.org/moin/PythonDecoratorLibrary</a></a></span><ul class="toc-item"><li><span><a href="#不使用-@wraps来保持原始函数的信息" data-toc-modified-id="不使用-@wraps来保持原始函数的信息-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>不使用 @wraps来保持原始函数的信息</a></span></li><li><span><a href="#利用装饰器定义属性" data-toc-modified-id="利用装饰器定义属性-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>利用装饰器定义属性</a></span></li><li><span><a href="#Memorize" data-toc-modified-id="Memorize-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Memorize</a></span></li><li><span><a href="#Alternate-memoize-as-nested-functions" data-toc-modified-id="Alternate-memoize-as-nested-functions-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>Alternate memoize as nested functions</a></span></li><li><span><a href="#Alternate-memoize-as-dict-subclass" data-toc-modified-id="Alternate-memoize-as-dict-subclass-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>Alternate memoize as dict subclass</a></span></li><li><span><a href="#Alternate-memoize-that-stores-cache-between-executions" data-toc-modified-id="Alternate-memoize-that-stores-cache-between-executions-3.6"><span class="toc-item-num">3.6&nbsp;&nbsp;</span>Alternate memoize that stores cache between executions</a></span></li><li><span><a href="#Cached-Properties" data-toc-modified-id="Cached-Properties-3.7"><span class="toc-item-num">3.7&nbsp;&nbsp;</span>Cached Properties</a></span></li><li><span><a href="#Retry" data-toc-modified-id="Retry-3.8"><span class="toc-item-num">3.8&nbsp;&nbsp;</span>Retry</a></span></li><li><span><a href="#Pseudo-curring" data-toc-modified-id="Pseudo-curring-3.9"><span class="toc-item-num">3.9&nbsp;&nbsp;</span>Pseudo-curring</a></span></li><li><span><a href="#Creating-decorator-with-optional-argument" data-toc-modified-id="Creating-decorator-with-optional-argument-3.10"><span class="toc-item-num">3.10&nbsp;&nbsp;</span>Creating decorator with optional argument</a></span></li><li><span><a href="#Controllable-DIY-debug" data-toc-modified-id="Controllable-DIY-debug-3.11"><span class="toc-item-num">3.11&nbsp;&nbsp;</span>Controllable DIY debug</a></span></li><li><span><a href="#Easy-adding-methods-to-a-class-instance" data-toc-modified-id="Easy-adding-methods-to-a-class-instance-3.12"><span class="toc-item-num">3.12&nbsp;&nbsp;</span>Easy adding methods to a class instance</a></span></li><li><span><a href="#Counting-function-calls" data-toc-modified-id="Counting-function-calls-3.13"><span class="toc-item-num">3.13&nbsp;&nbsp;</span>Counting function calls</a></span></li><li><span><a href="#Alternate-counting-function-calls" data-toc-modified-id="Alternate-counting-function-calls-3.14"><span class="toc-item-num">3.14&nbsp;&nbsp;</span>Alternate counting function calls</a></span></li><li><span><a href="#Generating-Deprecation-Warnings" data-toc-modified-id="Generating-Deprecation-Warnings-3.15"><span class="toc-item-num">3.15&nbsp;&nbsp;</span>Generating Deprecation Warnings</a></span></li><li><span><a href="#Smart-deprecation-warnings(with-valid-filenames,-line-number,-etc)" data-toc-modified-id="Smart-deprecation-warnings(with-valid-filenames,-line-number,-etc)-3.16"><span class="toc-item-num">3.16&nbsp;&nbsp;</span>Smart deprecation warnings(with valid filenames, line number, etc)</a></span></li><li><span><a href="#Ignoring-Deprecation-Warning" data-toc-modified-id="Ignoring-Deprecation-Warning-3.17"><span class="toc-item-num">3.17&nbsp;&nbsp;</span>Ignoring Deprecation Warning</a></span></li><li><span><a href="#Enable/Disable-Decorators" data-toc-modified-id="Enable/Disable-Decorators-3.18"><span class="toc-item-num">3.18&nbsp;&nbsp;</span>Enable/Disable Decorators</a></span></li><li><span><a href="#Easy-Dump-of-Function-Arguments" data-toc-modified-id="Easy-Dump-of-Function-Arguments-3.19"><span class="toc-item-num">3.19&nbsp;&nbsp;</span>Easy Dump of Function Arguments</a></span></li><li><span><a href="#Pre-/Post--Conditions" data-toc-modified-id="Pre-/Post--Conditions-3.20"><span class="toc-item-num">3.20&nbsp;&nbsp;</span>Pre-/Post- Conditions</a></span></li><li><span><a href="#Profiling/Coverage-Analysis" data-toc-modified-id="Profiling/Coverage-Analysis-3.21"><span class="toc-item-num">3.21&nbsp;&nbsp;</span>Profiling/Coverage Analysis</a></span></li><li><span><a href="#Line-Tracing-Individual-Functions" data-toc-modified-id="Line-Tracing-Individual-Functions-3.22"><span class="toc-item-num">3.22&nbsp;&nbsp;</span>Line Tracing Individual Functions</a></span></li><li><span><a href="#Synchronization" data-toc-modified-id="Synchronization-3.23"><span class="toc-item-num">3.23&nbsp;&nbsp;</span>Synchronization</a></span></li><li><span><a href="#Type-Enforcement-(accepts/returns)" data-toc-modified-id="Type-Enforcement-(accepts/returns)-3.24"><span class="toc-item-num">3.24&nbsp;&nbsp;</span>Type Enforcement (accepts/returns)</a></span></li><li><span><a href="#CGI-method-wrapper(略)" data-toc-modified-id="CGI-method-wrapper(略)-3.25"><span class="toc-item-num">3.25&nbsp;&nbsp;</span>CGI method wrapper(略)</a></span></li><li><span><a href="#State-Machine-Implementation" data-toc-modified-id="State-Machine-Implementation-3.26"><span class="toc-item-num">3.26&nbsp;&nbsp;</span>State Machine Implementation</a></span></li></ul></li></ul></div>

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


# ##### 摘自 https://wiki.python.org/moin/PythonDecoratorLibrary

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

# In[3]:


import sys
def test(a, b):
    #获取当前函数的局部变量
    print(sys._getframe(0).f_locals)
    #获取main的全部变量, 这里面包括:
    #1. 导入的模块
    #2. 用户定义的函数(def)
    print(sys._getframe(1).f_locals.keys())


# test(1, 3)


# In[9]:


import sys


def proget(func):
    locals_ = sys._getframe(1).f_locals
    print('\nIn proget:')
    print('locals: ', locals_)
    name = func.__name__
    prop = locals_.get(name)
    print('before set property: ', prop)
    if not isinstance(prop, property):
        prop = property(fget=func, doc=func.__doc__)
    else:
        doc = prop.__doc__ or func.__doc__
        prop = property(func, prop.fset, prop.fdel, doc)
    print('after set property: ', prop)
    return prop


def propset(func):
    locals_ = sys._getframe(1).f_locals
    print('\nIn proset:')
    print('locals: ', locals_)
    name = func.__name__
    prop = locals_.get(name)
    print('before set property: ', prop)
    if not isinstance(prop, property):
        prop = property(None, func, doc=func.__doc__)
    else:
        doc = prop.__doc__ or func.__doc__
        prop = property(prop.fget, func, prop.fdel, doc)
    print('after set property: ', prop)
    return prop


# In[10]:


#This canbe used like this.

class Example(object):
    
    @proget
    def myattr(self):
        return self._half * 2
    
    @propset
    def myattr(self, value):
        self._half = value / 2


# 也可以不用生成器--灵活运用 locals()

# In[11]:


class Example(object):
    def myattr():
        doc = """This is  the doc string."""     
        def fget(self):
            return self._half / 2
        def fset(self, value):
            self._half = value
        def fdel(self):
            del self._half
        
        return property(**locals())
    myattr = myattr()
        


# In[12]:


Example.__dict__


# 另一个装饰器的实现

# In[ ]:





# ###### Memorize

# In[19]:


import collections
import functools

class memorized(object):
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance
            # better to not cache than blow up
            return self.func(*args)
        if args in self.cache:
            print(f'{args} in cache.')
            return self.cache[args]
        else:
            print(f'{args} cached.')
            value = self.func(*args)
            self.cache[args] = value
            return value
    
    def __repr__(self):
        """Return the function's docstring"""
        return self.func.__doc__
    def __get__(self, instance, owner):
        print('calling __get__.')
        return functools.partial(self.__call__, instance)
        


# In[20]:


@memorized
def fib(n):
    if n in (0,1):
        return n
    return fib(n-1) + fib(n-2)


# In[21]:


print(fib(12))


# ###### Alternate memoize as nested functions

# In[22]:


def memorized(obj):
    cache = {}
    obj.cache = {}
    @functools.warps(obj)
    def memorizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memorizer


# ###### Alternate memoize as dict subclass

# In[23]:


class memorize(dict):
    """
    memorize 继承了字典类
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *args):
        return self[args]
    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


# ###### Alternate memoize that stores cache between executions

# In[54]:


import sys
import inspect
def func(a, b):
    """
    stack的最顶层, 即idx为零的元素, 储存了最近执行的那一行
    """
    frame = inspect.stack()
    # `frame = inspect.stack()`处的栈帧信息
    print(frame[0])
    print(sys._getframe(0))
    # `def func(a, b)`处的栈帧信息
    print(frame[1])
    print(sys._getframe(1))
    # func所在文件的栈帧信息
    print(frame[-1].filename)


# In[55]:


func(1, 3)


# In[5]:


import pickle
import collections
import functools
import inspect
import os.path
import re
import unicodedata


class Memorize(object):
    def __init__(self, func):
        self.func = func
        self._set_parent_filename()
        self.__name__ = self.func.__name__
        self._set_cache_filename()
        if self.cache_exists():
            self.read_cache()
            if not self.is_safe_cache():
                self.cache = {}
        else:
            self.cache = {}
    
    def __call__(self, *args):
        print('Call __call__ of Memorize.')
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        if args in self.cache:
            print('Find in cache.')
            return self.cache[args]
        else:
            print('Update cache.')
            value = self.func(*args)
            self.cache[args] = value
            self.save_cache()
            return value

    #在初始化的时候被调用
    def _set_parent_filename(self):
        """Set `self.parent_file` to the absolute path
        of the file containing the memorized function.
        """
        def filename_from_path(filepath):
            return filepath.split('/')[-1]
        print('Setting parent filename.')
        real_parent_file = inspect.stack()[-1].filename
        print('real_parent_file is: ', real_parent_file)
        self.parent_filepath = os.path.abspath(real_parent_file)
        print('parent_filepath is: ', self.parent_filepath)
        self.parent_filename = filename_from_path(real_parent_file)
    
    #在初始化的时候被调用
    def _set_cache_filename(self):
        """Set self.cache_filename to an os-compliant
        version of `file_function.cache`
        """
        def slugfy(value):
            """Normalizes string, convert to lowercase, removes
            non-alpha characters, and converts space to hyphens
            """
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
            value = re.sub(r'[^\w\s-]', '', value.decode('utf-8', 'ignore'))
            value = value.strip().lower()
            value = re.sub(r'[-\s]+', '-', value)
            return value
        filename = slugfy(self.parent_filename.replace('.py', ''))
        print('The filename is: ', filename)
        funcname = slugfy(self.__name__)
        self.cache_filename = filename + '_' + funcname + '.cache'
        print('The file is in:', self.cache_filename)
    
    #在is_safe_cache里被调用
    def get_last_update(self):
        """Return the time that the parent file was last 
        update
        """
        #获取文件被更改的次数
        last_update_time = os.path.getmtime(self.parent_filepath)
        return last_update_time
    
    # 在初始化的时候被调用
    def is_safe_cache(self):
        """Returns True if the file containing the memorized
        function has not been updated since the cache was
        last saved.
        """
        if self.get_last_update() > self.timestamp:
            return False
        else:
            return True
    
    # 在初始化的时候调用
    def read_cache(self):
        """
        Read a picked dictionary into self.timestamp and self.cache
        """
        with open(self.cache_filename, 'rb') as f:
            data = pickle.loads(f.read())
            self.timestamp = data['timestamp']
            self.cache = data['cache']
    
    # 在碰到没有出现过的参数的时候调用
    def save_cache(self):
        """Pickle the file's timestamp and function's cache
        in a dict object
        """
        with open(self.cache_filename, 'wb+') as f:
            out = dict()
            out['timestamp'] = self.get_last_update()
            out['cache'] = self.cache
            f.write(pickle.dumps(out))
    
    # 在初始化的时候调用
    def cache_exists(self):
        """Returns True if a matching cache exists in the current directory
        """
        if os.path.isfile(self.cache_filename):
            return True
        return False
    
    def __repr__(self):
        """Return the function's docstring
        """
        return self.func.__doc__
    
    def __get__(self, instance, owner):
        """Support instance methods
        """
        return functools.partial(self.__call__, instance)

            
        


# In[6]:


@Memorize
def f(a, b):
    return a+b


# In[7]:


f(1, 2)


# In[8]:


f(2, 4)


# In[9]:


f(1, 2)


# ###### Cached Properties

# In[26]:


import time
import random

class cached_property(object):
    """Decorator for read-only `properties` evaluated only once within TTL period.
    """
    def __init__(self, ttl=300):
        self.ttl = ttl

    #在定义 property.get的时候调用
    def __call__(self, func, doc=None):
        print('Call __call__.')
        self.func = func
        print(type(func))
        self.__doc__ = doc or func.__doc__
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        return self
    
    def __get__(self, instance, owner):
        now = time.time()
        try:
            value, last_update = instance._cache[self.__name__]
            if self.ttl > 0 and now - last_update > self.ttl: #recache
                print('Need recache.')
                raise AttributeError
        except (KeyError, AttributeError):
            value = self.func(instance) #调用实例的方法
            try:
                cache = instance._cache
            except AttributeError:
                cache = instance._cache = {}
            cache[self.__name__] = (value, now)
        return value
                


# In[27]:


class MyClass(object):
    # create property whose value is cached for ten minutes
    @cached_property(ttl=600)
    def randint(self):
        # will only be evaluated every 10 min. at maximum.
        return random.randint(0, 100)


# In[28]:


a = MyClass()
a.randint


# ###### Retry

# In[2]:


import time 
import math

def retry(tries, delay=3, backoff=2):
    """Retry a function or method until it returns True.
    """
    if backoff <= 1:
        raise ValueError('backoff must be greater than 1.')
    tries = math.floor(tries)
    if tries < 0:
        raise ValueError('tries must be 0 or greater.')
    if delay <= 0:
        raise ValueError('delay must be greater than 0.')
    
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            rv = f(*args, **kwargs)
            while mtries >0:
                if rv is True:
                    return True
                mtries -= 1
                # wait
                time.sleep(mdelay)
                # make future wait longer
                mdelay *= backoff
                # try again
                rv = f(*args, **kwargs)
            return False
        return f_retry # true decorator -> decorated function
    return deco_retry # @retry(arg[, ...]) -> true decorator
                


# ###### Pseudo-curring

# In[4]:


class curried(object):
    """Decorator that return a function that keeps returning 
    functions until all arguments are supplied; then the orginal
    function is evaluated.
    """
    def __init__(self, func, *args):
        self.func = args
        self.args = args
    def __call__(self, *args):
        args_ = self.args + args
        # 如果 当前的非关键字参数 少于func中的关键字参数
        # 就 递归地 return 一个 curried 对象
        if len(args_) < self.func.__code__.co_argcount:
            return curried(self.func, *args)
        else:
            return self.func(*args)            


# ###### Creating decorator with optional argument

# In[15]:


import functools, inspect

def decorator(func):
    """Allow to use decorator either with arguments or not.
    """
    def isFuncArg(*args, **kwargs):
        """判断参数是否只有一个, 且为(被装饰的)函数
        """
        return len(args) == 1 and len(kwargs) == 0        and (inspect.isfunction(args[0]) or isinstance(args[0], type))
    
    if isinstance(func, type):
        def class_wrapper(*args, **kwargs):
            if isFuncArg(*args, **kwargs):
                return func()(*args, **kwargs) # create a cls before use
            else:
                return func(*args, **kwargs)
        class_wrapper.__name__ = func.__name__
        class_wrapper.__module__ = func.__module__
        return class_wrapper
    
    else:
        print('被装饰的对象是函数.')
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            if isFuncArg(*args, **kwargs):
                print('装饰了函数: ', (args, kwargs))
                return func(*args, **kwargs)
            else:
                print('装饰了函数, 并且有参数: ', (args, kwargs))
                def functor(userFunc):
                    print(userFunc)
                    return func(userFunc, *args, **kwargs)
                return functor
        return func_wrapper


# In[16]:


@decorator
def apply(func, *args, **kwargs):
    """执行被装饰的函数
    """
    return func(*args, **kwargs)


# In[17]:


@apply
def test():
    return 'test'


# In[18]:


@apply(2, 3)
def test(a, b):
    return a + b


# ###### Controllable DIY debug

# In[27]:


import sys

WHAT_TO_DEBUG = set(['io', 'core']) # change to what you need

class debug(object):
    """Decorator which helps to control what aspects of program
    to debug on per-function basis. Aspects are provided as list
    of arguments. It DOSEN'T slowdown functions which aren't 
    supposed to be debugged.
    """
    def __init__(self, aspects=None):
        self.aspects = set(aspects)
    
    def __call__(self, func):
        if self.aspects and WHAT_TO_DEBUG:
            def new_func(*args, **kwargs):
                print(f'{func.__name__}, ({args}, {kwargs}).')
                func_result = func(*args, **kwargs)
                print(f'{func.__name__} returned {func_result}.')
                return func_result
            new_func.__doc__ = func.__doc__
            return new_func
        else:
            return func


# ###### Easy adding methods to a class instance

# In[28]:


import types
def add_method(instance):
    def decorator(func):
        func = types.MethodType(func, instance)
        setattr(instance, func.__name__, func)
        return func
    return decorator


# In[32]:


class Foo(object):
    def __init__(self):
        self.x = 42

foo = Foo()

@add_method(foo)
def print_x(self):
    print(self.x)

foo.print_x()


# ###### Counting function calls

# In[34]:


class countcalls(object):
    """Decorator that keeps track of the number of time
    a function is called.
    """
    __instances = {}
    
    def __init__(self, func):
        self.__func = func
        self.__numcalls = 0
        # Register the instance
        countcalls.__instances[func] = self
    
    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self.__func(*args, **kwargs)
    
    @staticmethod
    def count(func):
        return countcalls.__instances[func].__numcalls
    @staticmethod
    def counts():
        return dict([(f, countcalls.count(f))                     for f in countcalls.__instances])


# ###### Alternate counting function calls

# In[36]:


class countcalls(object):

    __instances = {}

    def __init__(self, func):
        self.__func = func
        self.__numcalls = 0
        countcalls.__instances[func] = self

    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self.__func(*args, **kwargs)

    def count(self):
        return countcalls.__instances[self.__func].__numcalls

    @staticmethod
    def counts():
        return dict([
            (f.__name__, countcalls.__instance[f].__numcalls)
            for f in countcalls.__instances
        ])


# ###### Generating Deprecation Warnings

# In[37]:


import warnings


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in warning being emitted
    when the function is used.
    """
    def new_func(*args, **kwargs):
        warnings.warn(
            'Call to deprecated function {}.'.format(func.__name__),
            category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


# ###### Smart deprecation warnings(with valid filenames, line number, etc)

# In[38]:


import warnings
import functools


def deprecated(func):
    
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            f'Call to deprecated function {func.__name__}.',
            category=DeprecationWarning,
            filename=func.__code__.co_filename,
            lineno=func.__code__.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func


# ###### Ignoring Deprecation Warning

# In[40]:


import warnings
import functools


def ignore_deprecation_warnings(func):
    """This is a decorator which can be used to 
    ignore deprecation warnings occurring in a function.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',
                                    category=DeprecationWarning)
            return func(*args, **kwargs)
    return new_func


# ###### Enable/Disable Decorators

# In[45]:


def unchanged(func):
    """This decorator dosen't add any behavior.
    """
    return func
def disabled(func):
    """This decorator disables the provided function, and does nothing.
    """
    def empty_func(*args, **kwargs):
        pass
    return empty_func

enabled  = unchanged


# In[47]:


GLOBAL_ENABLE_FLAG = True

state = enabled if GLOBAL_ENABLE_FLAG else disabled

@state
def foo():
    print('enabled.')


# ###### Easy Dump of Function Arguments

# In[85]:


def dump_args(func):
    """This decorator dumps out the arguments passed
    to a function before calling it.
    """
    argnames = func.__code__.               co_varnames[:func.__code__.co_argcount]
    fname = func.__name__
    
    def echo_func(*args, **kwargs):
        all_args = {(arg_name, arg_value)                    for arg_name, arg_value in zip(argnames, args)}
        all_args.update({(name, value)                         for name, value in kwargs.items()})
        # print(all_args)
        msg = f'{fname} : '
        msg += ', '.join('%s=%r' % entry                         for entry in all_args)
        print(msg)
        return func(*args, **kwargs)
    return echo_func


# In[86]:


def f(a, b, c):
    print (a + b + c)


# In[87]:


f.__code__.co_argcount


# In[88]:


f.__code__.co_varnames


# In[89]:


@dump_args
def func(a, b, c):
    return a + b + c


# ###### Pre-/Post- Conditions

# In[41]:


import types
import itertools
DEFAULT_ON = True


class FunctionWrapper(object):
    def __init__(self, precondition,
                 postcondition, function):
        self._pre = precondition
        self._post = postcondition
        self._func = function

    def __call__(self, *args, **kwargs):
        precondition = self._pre
        postcondition = self._post

        if precondition:
            precondition(*args, **kwargs)
        # 注意 _func 有可能是一个 FunctionWrapper 的实例,
        # 所以这里可能是一个递归调用
        result = self._func(*args, **kwargs)
        if postcondition:
            postcondition(result, *args, **kwargs)
        return result


class conditions(object):
    __slots__ = ('__precondition', '__postcondition')

    def __init__(self, pre, post,
                 use_conditions=DEFAULT_ON):
        if not use_conditions:
            pre, post = None, None
        self.__precondition = pre
        self.__postcondition = post

    def __call__(self, function):

        pres = set((self.__precondition, ))
        posts = set((self.__postcondition, ))

        while isinstance(function, FunctionWrapper):
            # 收集 pre 和 post conditions
            # 注意这里用 set 来过滤掉完全相同的 pre/post conditions
            pres.add(function._pre)
            posts.add(function._post)
            # while 循环直到拆包function到最后一层(获得被装饰的函数)
            # 终止
            function = function._func

        # filter out None conditions and
        # build pairs of pre and post conditions
        for pre, post in itertools.zip_longest(pres, posts):
            if pre or post:
                function = FunctionWrapper(pre, post, function)
        return function


def precondition(precondition, use_conditions=DEFAULT_ON):
    """precondition 检查函数的参数
    """
    return conditions(precondition, None, use_conditions)


def postcondition(postcondition, use_conditions=DEFAULT_ON):
    """post condition 检查函数的返回值
    """
    return conditions(None, postcondition, use_conditions)


# ###### Profiling/Coverage Analysis

# In[1]:


import atexit
import inspect
import logging
import os
import re
import sys

# For profiling
from profile import Profile
import pstats

# For timecall
import timeit

# # For hostsshot profiling (inaccurate!)
# # not available in Python 3
# try:
#     import hotshot
#     import hostshot.stats
# except ImportError:
#     hotshot = None

# For trace.py
import trace
import dis
import token
import tokenize

# # For hotshot coverage 
# # (inaccurate!; uses undocumented APIs; might break)
# # not available in Python 3
# if hotshot is not None:
#     import _hostshot
#     import hostshot.log

# For cProfile profiling (best)
try:
    import cProfile
except ImportError:
    cProfile = None


# In[2]:


# registry of available profilers
AVAILABLE_PROFILERS = {}


class FuncProfile(object):
    """Profiler for a function (uses profile).
    """
    # This flag is shared between all instance
    in_profiler = False

    Profile_ = Profile

    def __init__(self, func, skip=0, filename=None,
                 immediate=False, dirs=False,
                 sort=None, entries=40, stdout=True):
        """Create a profiler for a function.
        Every profiler has its own log file (the name of which 
        is derived from the function name).
        FuncProfile registers an atexit handler taht prints profiling
        information to sys.stderr when the program terminates.
        """
        self.func = func
        self.skip = skip
        self.filename = filename
        self._immediate = immediate
        self.stdout = stdout
        self.dirs = dirs
        self.sort = sort or ('cumulative', 'time', 'call')
        if isinstance(self.sort, str):
            self.sort = (self.sort, )
        self.entries = entries
        self.reset_stats()
        if not self.immediate:
            # 用于程序结束时的回调函数
            atexit.register(self.atexit)

    @property
    def immediate(self):
        return self._immediate

    def reset_stats(self):
        """Reset accumulated profiler statistics.
        """
        self.stats = pstats.Stats(Profile())
        self.ncalls = 0
        self.skipped = 0

    def print_stats(self):
        """Print profil information to sys.stdout.
        """
        stats = self.stats
        if self.filename:
            stats.dump_stats(self.filename)
        if self.stdout:
            funcname = self.func.__name__
            filename = self.func.__code__.co_filename
            lineno = self.func.__code__.co_firstlineno
            print("")
            print('*** PROFILER RESULTS ***')
            print(f'{funcname} ({filename}:{lineno})')
            if self.skipped:
                skipped = f'{self.skipped} calls not profiled.'
            else:
                skipped = 'without skipped.'
            print(f'Function called {self.ncalls} times, ',
                  skipped)
            print('')
            if not self.dirs:
                stats.strip_dirs()
            stats.sort_stats(*self.sort)
            stats.print_stats(self.entries)

    def atexit(self):
        """Stop profiling and print profile information
        to sys.stdout.
        This function is registered as an atexit hook.
        """
        self.print_stats()

    def __call__(self, *args, **kwargs):
        """Profile a single call to the function.
        """
        self.ncalls += 1
        if self.skip > 0:
            print(self.skip)
            self.skip -= 1
            print(self.skip)
            self.skipped += 1
            return self.func(*args, **kwargs)
        if FuncProfile.in_profiler:
            # handle recursive calls
            return self.func(*args, **kwargs)

        profiler = self.Profile_()
        try:
            FuncProfile.in_profiler = True
            return profiler.runcall(self.func, *args, **kwargs)
        finally:
            FuncProfile.in_profiler = False
            self.stats.add(profiler)
            if self.immediate:
                self.print_stats()
                self.reset_stats()


AVAILABLE_PROFILERS['profile'] = FuncProfile


# In[3]:


# __all__ = ['coverage', 'coverage_with_hotshot',
#            'profile', 'timecall']
import functools
def profile(func=None, skip=0, 
            filename=None, immediate=False, 
            dirs=False, sort=None, 
            entries=40, stdout=True,
            profiler=('cProfile', 'profile', 'hotshot')):
    """Mark `func` for profiling.
    
    If `skip` is > 0, first `skip` calls to `func` will
    not be profiled.
    
    If `immediate` is False, profiling results will be
    printed to sys.stdout on program termination. Otherwise
    results will be printed after each call. (If you don't
    want this, set stdout=False and specify a `filename`
    to store profile data.)
    
    If `dirs` is False only the name of the file will be
    printed. Otherwise the full path is used.
    
    `sort` can be a list of sort keys (defaulting to ['cumulative',
    'time', 'calls']).  The following ones are recognized::

        'calls'      -- call count
        'cumulative' -- cumulative time
        'file'       -- file name
        'line'       -- line number
        'module'     -- file name
        'name'       -- function name
        'nfl'        -- name/file/line
        'pcalls'     -- call count
        'stdname'    -- standard name
        'time'       -- internal time
    
    `entries` limites the output to the first N entries.
    
    `profiler` can be used to selected the preferred profiler,
    or specify a sequence of them, in order of preference. The
    default is 'cProfile', 'profile', 'hotshot').
    
    If `filename` is specified, the profile stats will be
    stored in the named file. You can load then with 
    pystats.Stats(filename) or use a visualization tool 
    like RunSnakeRun.    
    """
    if func is None: # We are a decorator marker
        def decorator(func):
            return profile(func, skip=skip, 
                           filename=filename, immediate=immediate,
                           dirs=dirs, sort=sort,
                           entries=entries, profiler=profiler,
                           stdout=stdout)
        return decorator
    else: # We are a decorator
        if isinstance(profiler, str):
            profiler = [profiler]
        
        for p in profiler:
            if p in AVAILABLE_PROFILERS:
                profiler_class = AVAILABLE_PROFILERS[p]
                break
        else:
            raise ValueError('Only these profilers are available: %s'                             % ', '.join(sorted(AVAILABLE_PROFILERS)))

        if not profiler_class:
            raise ValueError('The `profiler_class` is None.'
                             'Please check `AVAILABLE_PROFILERS`.')
        
        func_profiler = profiler_class(func, skip=skip, 
                                filename=filename,immediate=immediate, 
                                dirs=dirs, sort=sort, 
                                entries=entries, stdout=stdout)
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            return func_profiler(*args, **kwargs)
        return new_func  


if cProfile is not None:
    class CProfileFuncProfile(FuncProfile):
        Profile_ = cProfile.Profile
    AVAILABLE_PROFILERS['cProfile'] = CProfileFuncProfile


# In[4]:


class TraceFuncCoverage(object):
    """Coverage analysis for a function (use trace module)
    """

    # Shared between all instances so that nested calls work
    tracer = trace.Trace(count=True, trace=True,
                         ignoredirs=[sys.prefix, sys.exec_prefix])

    # This flag is also shared between all instances
    tracing = False

    def __init__(self, func):
        """Create a profiler for a function.
        Every profiler has its own log file (the name of which is derived from the function name).
        TraceFuncCoverage registers an atexit hander that prints profiling information to sys.stderr
        when the program terminates.
        The log file is not removed and remains there to clutter the current working directory.
        """
        self.func = func
        self.logfilename = f'{func.__name__}.{os.getpid()}.cprof'
        self.ncalls = 0
        atexit.register(self.atexit)

    def __call__(self, *args, **kwargs):
        """Profile a singe call to the function.
        """
        self.ncalls += 1
        if TraceFuncCoverage.tracing:  # pragma: nocover
            return self.func(*args, **kwargs)
        old_trace = sys.gettrace()
        try:
            TraceFuncCoverage.tracing = True
            return self.tracer.runfunc(self.func, *args, **kwargs)
        finally:  # progma: nocover
            sys.settrace(old_trace)
            TraceFuncCoverage.tracing = False

    def atexit(self):
        """Stop profiling and print profile information to sys.stderr
        This function is registered as an atexit hook.
        """
        funcname = self.func.__name__
        filename = self.func.__name__.co_filename
        lineno = self.func.__name__.co_firstlineno
        print('')
        print('***COVERAGE RESULT***')
        print(f'{funcname} ({filename} : {lineno})')
        print(f'Function called {self.ncalls} times.')
        print('')

        # TO DO: 实现 FuncSource 类
        function_source = FuncSource(self.func)
        for (filename, lineno), count in self.tracer.counts.items():
            if filename != function_source.filename:
                continue
            function_source.mark(lineno, count)
        print(function_source)
        never_executed = function_source.count_never_executed()
        if never_executed:
            print(f'{never_executed} lines were not executed.')


class FuncSource(object):
    pass


# ###### Line Tracing Individual Functions

# In[13]:


import sys
import os
import linecache


def trace(func):
    def globaltrace(frame, why, arg):
        if why == 'call':
            return localtrace
        else:
            return None

    def localtrace(frame, why, arg):
        if why == 'line':
            # record the file name and line number of every trace
            filename = frame.f_code.co_filename
            # 函数最后一行
            lineno = frame.f_lineno

            basename = os.path.basename(filename)
            print(f'{basename}({lineno}) '
                  f': {linecache.getline(filename, lineno)}')
        return localtrace

    def _func(*args, **kwargs):
        sys.settrace(globaltrace)
        result = func(*args, **kwargs)
        sys.settrace(None)
        return result
    return _func


# ###### Synchronization

# In[16]:


# Synchronize two (or more) functions on a given lock.
from threading import Lock
def synchronized(lock):
    """Synchronization decorator
    """
    def wrap(func):
        def new_func(*args, **kwargs):
            lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                lock.release()
        return new_func
    return wrap


# In[17]:


# Example usage:

my_lock = Lock()


@synchronized(my_lock)
def call(*args):
    pass


@synchronized(my_lock)
def call2(*args):
    pass


# ###### Type Enforcement (accepts/returns)

# In[40]:


import sys

def info(fname, expected, actual, flag):
    """Convenience function returns nicely formatted error/warning msg.
    """
    fmt = lambda types: ', '.join([str(t).split('\'')[1] for t in types])
    expected, actual = fmt(expected), fmt(actual)
    msg = f'`{fname}` method ' +          ('accepts', 'returns')[flag] + f'({expected}) but ' +          ('was given', 'result is')[flag] + f'({actual}).'
    return msg

def accepts(*types, **kwargs):
    """Function decorator. Checks decorated function's arguments are
    of the expected types.
    
    Paramsters:
    -----------
    types: The expected types of the inputs to the decorated function.
           Must specify type for each parameter.
    kwargs: Optional specification of `debug` level (this is the only valid
            keyword argument, no other should be given).
            debug = (0 | 1 | 2)
    """
    if kwargs == dict():
        debug = 1
    else:
        debug = kwargs['debug']
    
    try:
        def decorator(func):
            def new_func(*args):
                if debug == 0:
                    return func(*args)
                assert len(args) == len(types)
                argtypes = tuple(map(type, args)) # 666
                if argtypes != types:
                    msg = info(func.__name__, types, argtypes, 0)
                    if debug == 1:
                        print(f'TypeWarning : {msg}.', file=sys.stderr)
                    elif debug == 2:
                        raise TypeError(msg)
                return func(*args)
            new_func.__name__ = func.__name__
            return new_func
        return decorator
    
    except KeyError as e:
        raise KeyError(e)
    except TypeError as e:
        raise TypeError(e)

def returns(return_type, **kwargs):
    """Function decorator. Check decorated function's return value is of the expected type.
    """
    try:
        if kwargs == dict():
            # dafault level: MEDIUM
            debug = 1
        else:
            debug = kwargs['debug']
        
        def decorator(func):
            def new_func(*args):
                result = func(*args)
                if debug == 0:
                    return result
                res_type = type(result)
                if res_type != return_type:
                    msg = info(f.__name__, (return_type, ), (res_type, ), 1)
                    if debug == 1:
                        print(f'TypeWarning : {msg}.', file=sys.stderr)
                    elif debug == 2:
                        raise TypeError(msg)
                return result
            new_func.__name__ = func.__name__
            return new_func
        return decorator
    except KeyError as e:
        raise KeyError(e)
    except TypeError as e:
        raise TypeError(e)


# In[41]:


@accepts(int, int, int)
@returns(float)
def average(x, y, z):
    return (x + y + z) / 3


# In[42]:


average(1, 3, .5)


# ###### CGI method wrapper(略)

# ###### State Machine Implementation

# In[ ]:


import types
import itertools

import logging
logging.basicConfig(filename="gf_info.txt",
    format = "%(levelname)-10s %(message)s",
    level = logging.ERROR)
from functools import wraps

def truncated(alist, cmprsn):
    for x in alist:
        if x.__name__ == cmprsn:
            break
        yield x

class ContextBase(object):
    pass

class _StateVariable(object):
    """Attribute of a class to maintain state.
    State Variable objects are instantiated indirectly via calls to the
    TransitionTable class's initialize method. TransitionTable objects are
    created at the class level.
    """
    def __init__(self, transTable, context):
        self.__current_state = transTable.initialstate
        self.__next_state = transTable.initialstate
        self.sTable = transTable
        self.__statestack = []
        self.__ctxClass = context.__class__
    
    def toNextState(self, context):
        """Transition to next state, if a next_state is different.
        In addition to the actual state transition, it invokes onLeave
        and onEnter methods as required.
        """
        if self.__next_state is not self.__current_state:
            cc = context.__class__
            tt_name = self.sTable.inst_state_name
            logging.debug(f'Transitioning to state {self.__next_state.__name__}.')
            
            def callInState(methName, curr_state):
                pass

