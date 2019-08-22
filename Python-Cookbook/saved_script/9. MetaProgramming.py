#!/usr/bin/env python
# coding: utf-8

# ###### 4. 定义带参数的装饰器

# In[53]:


from functools import wraps
import logging
logging.basicConfig(level=logging.DEBUG)
def logged(level, name=None, message=None):
    def decorator(func):
        logname = name if name else func.__name__
        log = logging.getLogger(logname)
        # log.setLevel(logging.INFO)
        logmsg = message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# In[54]:


@logged(logging.INFO)
def add(x, y):
    return x + y


# In[55]:


add(1, 3)


# ###### 5. 可自定义属性的装饰器

# <center>下面是下一个装饰器, 允许用户提供参数在运行时控制装饰器行为</center>
# 
# 1. attach_wrapper 是一个通过装饰器, 为一个 python object set attribute. 注意如果 func 为空, 那么返回一个绑定了 obj 参数的偏函数.
# 2. 当用来装饰函数时, logged 装饰器返回 decorate 函数对象, 用它来修饰被装饰的函数.
# 3. decorate 返回一个 **可变对象wrapper**, 在decorate内部定义的函数为wrapper对象绑定了两个方法. ***务必注意这种动态绑定attribute的方法***
# 4. 注意 set\_level 和 set\_msg 内部通过 nonlocal 来改变外部函数的局部变量 

# In[2]:


from functools import wraps, partial
import logging

# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


# In[13]:


def logged(level, name=None, message=None):
    """Add logging to a function. level is the logging
    level, name is the logger name, and message is the 
    log message. If name and message are not specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        
        #Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(new_level):
            nonlocal level
            level = new_level
        
        @attach_wrapper(wrapper)
        def set_msg(newmsg):
            nonlocal logmsg
            logmsg = newmsg
        return wrapper
    print('Return decorate when package the function.')
    return decorate
        


# In[14]:


@logged(logging.DEBUG)
def add(x, y):
    return x + y


# In[15]:


import logging
logging.basicConfig(level=logging.DEBUG)
add(2, 3)


# 值得注意的是: 你的访问函数会在多层装饰器之间传播, 如果你的装饰器都使用了 functools.wraps 注解

# In[24]:


import time
from functools import wraps
def timethis(func):  
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result
    return wrapper


# In[25]:


@timethis
@logged(logging.DEBUG)
def countdown(n):
    while n > 0:
        n -= 1


# In[26]:



countdown(1000000)

#访问函数依然可用
countdown.set_level(logging.WARNING)
countdown.set_msg("Counting down to zero")
countdown(1000000)


# 即使装饰器以相反的方向排放, 也是可以的~~~

# In[28]:


@logged(logging.DEBUG)
@timethis
def countdown(n):
    while n > 0:
        n -= 1


# 你也可以直接赋值属性, 但是这种方法只有 logged 是最外层装饰器时才有用.如果它的上面还有另外的装饰器(比如上面提到的 @timethis 例子)，那么它会隐藏底层属性，使得修改它们没有任何作用。 而通过使用访问函数就能避免这样的局限性。

# In[30]:


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__     
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        
        wrapper.level = level
        wrapper.logmsg = logmsg
        wrapper.log = log       
        return wrapper
    return decorate


# ###### 6. 带可选参数的装饰器

# In[33]:


#实现一个装饰器, 可以不传递参数给它, 也可以传递参数给它
from functools import wraps, partial
import logging

def logged(func=None, 
           *, 
           level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)
    logname = name if name else func.__name__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__
    
    @wraps
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)
    return wrapper


# 注意下面第二个调用, 最开始 func 参数没有被传递进来, 因为在 logged 装饰器函数中他必须是***可选的***, 这同时会迫使其他参数必须使用关键字指定!!! 同时我们使用了***偏函数技巧***, 让 logged 函数在 func 为空时返回一个包装的偏函数, 除了 func 参数以外其他所有的参数都确定下来了.

# In[ ]:


# 等价于 logged(func=add)
@logged
def add(x, y):
    return x + y 

#等价于 logged(level=logging.CRITICAL, name='example')(spam)
@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')


# ###### 7 利用装饰器实现类型检查
# ***需要 inspect 模块***

# In[43]:


from inspect import signature
def test_f(a, b):
    return 1


# In[52]:


s = signature(test_f)
s.bind(int, b=float).arguments


# In[54]:


#我们希望对函数的参数进行类型检查/断言
from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in oprimized mode, disable type checking.
        if not __debug__:
            return func
        #Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # 强制类型检查
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.\
                            format(name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate          


# In[55]:


@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)


# In[59]:


spam(1,2,3)
spam(1, 'hello', 3)
try:
    spam(1, 'hello', 'world')
except TypeError as e:
    print(e)


# <center>总结</center>
# 
# 1. 首先，装饰器只会在函数定义时被调用一次。 
# 2. 有时候你去掉装饰器的功能，那么你只需要简单的返回被装饰函数即可。上面的代码中，
#    如果全局变量　\_\_debug\_\_ 被设置成了False(当你使用-O或-OO参数的优化模式执行程序时)， 那么就直接返回未修改过的函数本身。
# 3. 装饰器的开始部分，我们使用了 bind_partial() 方法来执行从指定类型到名称的部分绑定。**注意你可以注意到缺失的参数被忽略了**。
# 4. 在装饰器创建的实际包装函数中使用到了 sig.bind() 方法。 bind() 跟 bind_partial() 类似，**但是它不允许忽略任何参数**。

# ###### 8.装饰器定义为类的一部分

# In[61]:


from functools import wraps
class A(object):
    #实例方法的装饰器
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)
        return wrapper
    #类方法的装饰器
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)
        return wrapper


# ###### 9.装饰器定义为类
# ***你需要自己实现 \_\_call\_\_和 \_\_get\_\_ 方法***

# In[1]:


import types
from functools import wraps
import sys
import inspect
class Profiled(object):
    def __init__(self, func):
        wraps(func)(self)
        print(inspect.signature(self.__wrapped__))
        self.ncalls = 0
    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        print('In __Call__.')
        #注意 args 的第一个参数 是 spam的实例化
        print(sys._getframe(0).f_locals['args'])
        return self.__wrapped__(*args, **kwargs)
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            # self(bar) 是 Profiled 的实例
            # instance 是 点运算符表达式左边的对象, 是 spam 的实例
            print('In __get__:',self, instance)
            print('After __get__:', 
                  types.MethodType(self, instance))
            #返回一个绑定的方法, 第一个参数是 spam的实例,
            #这里这个方法 是 Profiled 的实例,
            #接下来调用call方法的第一个参数就是 spam的实例了
            
            return types.MethodType(self, instance)


# 你可以在类外面或者里面使用 Profiled 装饰器

# In[2]:


@Profiled
def add(x, y):
    return x + y

class spam(object):
    # Profiled 是装饰器类, Profiled(bar) 是 Profiled的实例. 因而它是类方法.
    # Profile初始化时, wrap了 bar 方法. ！！！注意 bar 是实例方法, 它的第一个
    # 参数是 self!!!!!
    
    # 所以如果不提供 __get__ 方法, spam().bar 返回的是 Profiled 的实例, 
    # spam().bar(3) 缺少了 self 参数!!!!
    # 但是 spam().bar(spam(), 3) 就可以了。。。。
    @Profiled
    def bar(self, x):
        print('In bar :', (self, x))


# In[3]:


spam.bar.__dict__


# In[5]:


a = spam()


# In[6]:


a.bar


# In[21]:


a.bar(a, 3)


# In[255]:


add(2, 3)
add(4, 5)
add(5,7)
print(add.ncalls)


# In[257]:


s = spam()
s.bar(1)
s.bar(2)


# In[221]:


s.bar.ncalls
#因为 bar是类方法(描述符), 所以需要用类来调用它
spam.bar.ncalls


# In[201]:


class A(object):
    def __init__(self):
        pass
a1 = A()
a2 = A()
def grok(self, x):
    print('self is:', self)
    print('x is:', x)


# In[202]:


# __get__ 方法将 grok 函数与 class A 的实例 a 绑定在一起
# __get__ 方法的第一个参数与 a绑定
f = grok.__get__(a1, A)


# In[203]:


f


# In[204]:


f(1)


# In[205]:


types.MethodType(grok, a2)


# <center>总结</center>
# 
# 1. 注意 spam 的 bar 函数 是一个 ***Profiled 的实例***, 因而他是一个***类方法***, 
# 当你调用它时, 会根据***描述符协议***调用 Profiled 的 \_\_get\_\_ 方法. 这一方法的目的是创建一个绑定方法的对象
# 2. \_\_get\_\_方法为了确保绑定方法对象能被正确的创建. 因而我们自己实现的 \_\_get\_\_ 方法 用 type.MethodType 手动创建一个绑定的方法. 只有当spam的实例被使用的时候绑定方法才会被创建. 如果这个方法是在spam类上面来访问， 那么 \_\_get\_\_() 中的instance参数会被设置成None并直接返回 Profiled 实例本身。 这样的话我们就可以提取它的 ncalls 属性了。

# ###### 10. 为类和静态方法提供装饰器
# 确保装饰器在 @classmethod 或 @staticmethod 之前(此二者是最外层)

# In[1]:


import time
from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r
    return wrapper


class Spam(object):
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1


# In[2]:


from abc import ABCMeta, abstractmethod
class A(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def method(cls):
        pass


# ###### 11 装饰器未被包装函数增加参数
# ***需要 inspect 模块***

# In[8]:


from functools import wraps
from inspect import Parameter, getargspec, signature

def optional_debug(func):
    if 'debug' in signature(func).parameters:
        raise TypeError('debug argument already defined.')
    #wrapper 为 func 增加了一个 debug 参数
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)
    
    #修改wrapper的签名:
    ##获取func的签名
    sig = signature(func)
    params = list(sig.parameters.values())
    ##增加`debug`参数, 替换签名
    params.append(Parameter('debug', Parameter.KEYWORD_ONLY, default=False))
    wrapper.__signature__ = sig.replace(parameters=params)
    return wrapper

@optional_debug
def a(x):
    pass

@optional_debug
def b(x, y, z):
    pass        


# ###### 12. 使用装饰器扩充类的功能

# In[ ]:


def log_getattribute(cls):
    #获得原始的 __getattribute__
    orig_getattribute = cls.__getattribute__
    
    #实现自己的__getattribute__
    def new_attribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = new_attribute
    return cls


# ###### 13. 使用元类控制实例的创建

# 实现无实例化的类

# In[28]:


class NoInstance(type):
    def __call__(self, *args, **kwargs):
        print('NoNoNo.')
        raise TypeError('无法实例化!')


# In[29]:


class Spam(object, metaclass=NoInstance):
    @staticmethod
    def gtok(x):
        print('汪汪汪!')    
    def __call__(self):
        print('娃哈哈!')


# In[30]:


try:
    Spam()
except TypeError as e:
    print(e)


# <center>总结</center>
# 
# 1. type是一个元类。type就是Python在背后用来创建所有类的元类
# 2. Spam 是 type的实例化, 因此 Spam()会调用 type的__call__方法, 如果元类重写了__call__方法, 就会调用元类的__call__方法.

# 实现单类

# In[7]:


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


# In[8]:


class Spam(object, metaclass=Singleton):
    pass

assert Spam() is Spam()


# ###### 14. 捕捉类的启动顺序

# In[20]:


from collections import OrderedDict


class Typed(object):
    _excepted_type = type(None)

    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
#         print(self._excepted_type)
        if not isinstance(value, self._excepted_type):
            raise TypeError('Expected ' + str(self._excepted_type))
        instance.__dict__[self._name] = value


class Integer(Typed):
    _excepted_type = int


class Float(Typed):
    _excepted_type = float


class String(Typed):
    _excepted_type = str


# In[21]:


class OrderedMeta(type):
    """用元类来捕捉描述符的定义顺序
    """
    @classmethod
    def __prepare__(cls, class_name, bases):
        """__prepare__函数返回一个 OrderDict,
        然后所有类属性被加到这个OrderDict中.
        """
        return OrderedDict()
    def __new__(cls, class_name, bases, class_dict):
        d_ = dict(class_dict)
        order = []
        # 遍历 class_dict(这是OrderedDict的实例),
        # 把 Typed 的描述符加入到按照顺序加入到 order中
        # 更新字典(注意不能在 OrderedDict上更新)
        for name, value in class_dict.items():
            if isinstance(value, Typed):
                value._name = name
                order.append(name)
        d_['_order'] = order
        return super().__new__(cls, class_name, bases, d_)

class Structure(object, metaclass=OrderedMeta):
    def as_csv(self):
        return ','.join(str(getattr(self, name))                        for name in self._order)


# In[24]:


class Stock(Structure):
    name = String()
    price = Float()
    shares = Integer()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


# In[25]:


s = Stock('zzj', 100, 12.3)

s.as_csv()


# ###### 15. 定义有可选参数的元类

# In[5]:


# 你想定义一个元类, 允许使用它的类在定义时提供可选参数,
# 这样可以控制或者配置类型的创建过程

#你需要用强制关键字参数
#并且需要同时提供__init__ 和 __new__ 方法, 并且需要提供对应的参数签名
class MyMeta(type):

    # Optional
    @classmethod
    def __prepare__(cls, class_name, bases, *,
                    debug=False, synchronize=False):
        # Do something here.
        return super().__prepare__(class_name, bases)

    # Required
    def __new__(cls, class_name, bases, class_dict, *,
                debug=False, synchronize=False):
        return super().__new__(cls, class_name, bases, class_dict)

    # Required
    def __init__(cls, class_name, bases, class_dict, *,
                 debug=False, synchronize=False):
        super().__init__(class_name, bases, class_dict)


# In[6]:


# 使用
class Spam(metaclass=MyMeta, debug=True, synchronize=False):
    pass


# ###### \*args 和 \*\*kwargs 的强制参数签名

# In[10]:


from inspect import Signature, Parameter

# Make a signature for a func(x, y=42, *, z=None):
params = [Parameter(name='x', 
                    kind=Parameter.POSITIONAL_OR_KEYWORD),
          Parameter(name='y', 
                    kind=Parameter.POSITIONAL_OR_KEYWORD, 
                    default=42),
          Parameter(name='z', 
                    kind=Parameter.KEYWORD_ONLY,
                    default=None)
         ]
sig = Signature(parameters=params)

print(sig)


# In[11]:


# 一旦你有了一个签名对象, 你可以使用它的 bind 方法很容易的
# 将他绑定到 *args 和 **kwargs 中
def func(*args, **kwargs):
    bound_values = sig.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
        print(f'{name} : {value}')

func(1, 2, z=3)
func(y=2, x=1)


# 可以看出来，通过将签名和传递的参数绑定起来，可以强制函数调用遵循特定的规则，比如必填、默认、重复等等。

# In[14]:


#在看一个更加具体的例子

from inspect import Signature, Parameter

def make_sig(*names):
    params = [Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD)              for name in names]
    return Signature(params)


class Structure(object):
    __signature__ = make_sig()
    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)


# In[15]:


#Example use
class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')

class Point(Structure):
    __signature__ = make_sig('x', 'y')


# In[16]:


import inspect
print(inspect.signature(Stock))


# 在我们需要构建通用函数库、编写装饰器或实现代理的时候，对于 \*args 和 \*\*kwargs 的使用是很普遍的。 但是，这样的函数有一个缺点就是当你想要实现自己的参数检验时，代码就会笨拙混乱。这时候我们可以通过一个签名对象来简化它。

# In[20]:


# 我们可以把 Structure 中的 __signature__ 挪到元类中构造
class StructureMeta(type):
    def __new__(cls, class_name, bases, class_dict):
        class_dict['__signature__'] =             make_sig(*class_dict.get('_fields', []))
        return super().__new__(cls, class_name, bases, class_dict)


class Structure(object, metaclass=StructureMeta):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)


class Stock(Structure):
    _fields = ['name', 'shares', 'price']


# In[21]:


import inspect
print(inspect.signature(Stock))


# ###### 17. 在类上强制使用编程规约
# 你的程序包含一个很大的类继承体系，你希望强制执行某些编程规约（或者代码诊断）来帮助程序员保持清醒。
# 你可以自定义元类, 并且让它至于你的程序的最顶层。

# In[23]:


class NoMixedCaseMeta(type):
    """这个元类控制了属性的命名风格
    """
    def __new__(cls, class_name, bases, class_dict):
        for name in class_dict:
            if name.lower() != name:
                raise TypeError(f'Bad attribute name: {name}')
        return super().__new__(cls, class_name, bases, class_dict)

class Root(metaclass=NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self):
        pass
# class B(Root):
#     def fooBar(self):
#         pass


# In[ ]:


#下面的元类用来检测重载方法, 保证子类和父类中他们有相同的签名

from inspect import signature
import logging


class MatchSignaturesMeta(type):
    def __new__(cls, class_name, bases, class_dict):
        print('Run __new__.')
        print(cls)
        print(class_name)
        print(bases)
        print(class_dict)
        return super().__new__(cls, class_name, bases, class_dict)

    def __init__(cls, class_name, bases, class_dict):
        print('Run __init__.')
        print(cls)
        print(class_name)
        print(bases)
        print(class_dict)
        super().__init__(class_name, bases, class_dict)
        #
        sup = super(cls, cls)
        print(sup)
        for name, value in class_dict.items():
            if name.startswith('_') or not callable(value):
                continue
            # Get the previous defination (if any) and
            # compare the signatures
            previous_func = getattr(sup, name, None)
            if previous_func is not None:
                previous_sig = signature(previous_func)
                current_sig = signature(value)
                if previous_sig != current_sig:
                    logging.warning(
                        f'Signature mismatch in {value.__qualname__}:'
                        f'{previous_sig} != {current_sig}')


# 在元类中选择重新定义 \_\_new\_\_() 方法还是 \_\_init\_\_() 方法取决于你想怎样使用结果类。 \_\_new\_\_() 方法在类创建之前被调用，通常用于通过某种方式（比如通过改变类字典的内容）修改类的定义。 而 \_\_init\_\_() 方法是在类被创建之后被调用，当你需要完整构建类对象的时候会很有用。

# In[33]:


class Root(object, metaclass=MatchSignaturesMeta):
    pass


# In[36]:


class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass

# Class with redefined methods, but slightly different signatures
class B(A):
    def foo(self, a, b):
        pass

    def spam(self,x,z):
        pass


# In[ ]:




