#!/usr/bin/env python
# coding: utf-8

# 1. 属性描述符本质上是**类方法**.
# 2. 和 property 一样. 实例的点运算操作会优先 access 描述符.

# In[1]:


class Quantity(object):
    """区别于生成 Property 的工厂函数,
    这里使用属性描述符
    """

    def __init__(self, storage_name):
        self.storage_name = '__' + storage_name

    def __set__(self, instance, value):
        print('Calling setter.')
        if value > 0:
            # instance.__dict__[self.storage_name] = value
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')

    def __get__(self, instance, instance_type):
        print('calling getter.')
        return instance.__dict__[self.storage_name]


class LineItem(object):
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    @property
    def subtotal(self):
        return self.weight * self.price


# In[2]:


x = LineItem('zzj', 90, 450)
print(x.__dict__)
print(x.weight)


# In[3]:


# 这一版的代码我们自动生成属性的名字.
# 我们希望:
#     weight = Quantity()
#     price = Quantity()
# 而不是:
#     weight = Quantity('weight')
#     price = Quantity('price')


class Quantity(object):
    # 这个类成员是为了区分名字
    __num_instance = 0

    def __init__(self):
        
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__num_instance
        # 自己造一个属性名 ->_->
        self.storage_name = f'__{prefix}_{index}'
        cls.__num_instance += 1

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')

    @classmethod
    def counter(cls):
        return cls.__num_instance


class LineItem(object):
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    @property
    def subtotal(self):
        return self.weight * self.price


# In[4]:


x = LineItem('zzj', 90, 450)
print(x.__dict__)
print(x.weight)
print(Quantity.counter())


# ###### A New Descriptor Type
# 
# ![img/20_1.png](img/20_1.png)

# In[11]:


import abc


class AutoStorage(object):
    """Descriptor class that manages storage attributes automatically.
    实现了基本的 get 和 set 方法
    """
    __counter = 0

    def __init__(self):
        # 初始化函数生成一个唯一的字符串, 它是私有实例属性的名字
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = f'__{prefix}_{index}'
        cls.__counter += 1

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


# In[12]:


# 通常称 override 了 set 方法的描述符为 override descriptor
class Validated(abc.ABC, AutoStorage):
    """AutoStorage abstract subclass that overrides the __set__ method, 
    calling a validate method that must be implemented by subclasses.
    """

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        raise NotImplementedError


# In[13]:


# Quantity 和 NonBlank 继承了 抽象类 Validated,
# 实现了 validate 方法.
# 注意: validate 方法的返回方式在 Validated 中被限制了.


class Quantity(Validated):
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0.')
        else:
            return value


class NonBlank(Validated):
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank.')
        else:
            return value


# In[14]:


class LineItem(object):
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    @property
    def subtotal(self):
        return self.weight * self.price


# In[23]:


a = LineItem('zzj', 3, 4)

LineItem.__dict__['weight'].__dict__

b = LineItem('zzj2', 3.5, 4.5)

LineItem.__dict__['weight'].__dict__

print(a.__dict__)

print(b.__dict__)


# ###### Overriding Versus Nonoverriding Descriptors

# In[24]:


# 让我们定义一些辅助函数


def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__({pseudo_args})')


# In[25]:


class Overriding(object):
    """A typical overriding despritor with get and set
    """

    def __get__(self, instance, instance_type):
        print_args('get', self, instance, instance_type)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet(object):
    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding(object):
    def __get__(self, instance, instance_type):
        print_args('get', self, instance, instance_type)


# In[40]:


class Managed(object):
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()
    def spam(self):
        print(f'-> Managed.spam({display(self)})')


# In[27]:


# 让我们测试
obj = Managed()

# 下面两个点表达式都触发了描述符的 get 方法
print(obj.over)
print(Managed.over)

# 赋值语句触发了描述符的 set 方法
obj.over = 7
print(obj.over)

# 访问实例的 dict 不会触发同名的描述符的任何方法
obj.__dict__['over'] = 8
print(vars(obj))
print(obj.over)


# In[31]:


# 让我们测试
obj = Managed()

# 对于没有实现 get 方法的描述符, 下面
# 两个调用都会返回类属性本身
print(obj.over_no_get)
print(Managed.over_no_get)

obj.over_no_get = 7
print(obj.over_no_get)

# 因为 over_no_get 描述符没有实现 get 方法
# 所以当你添加了同名的实例属性后
# 点运算符会屏蔽掉同名的描述符
# 但是赋值语句仍然会调用描述符的 set 方法
obj.__dict__['over_no_get'] = 9
print(obj.over_no_get)
obj.over_no_get = 11


# In[33]:


# 让我们测试
obj = Managed()

# 对于只实现了 get 方法的描述符, reading 会调用 get 方法
print(obj.non_over)
# 但是赋值语句会直接创建一个
# 同名的实例对象.
# 然后这个同名的实例属性就会覆盖掉描述符的 get 方法!!!
obj.non_over = 7
print(obj.non_over)

# 但是在类上调用之可以正常访问
print(Managed.non_over)
# del 语句会删除实例对象
del obj.non_over
print(obj.non_over)


# **Overwriting a descriptor in the class**
# Class.XXX 会调用相关描述符的__get__方法, 并且优先级高于同名的类属性; 但 Class.XXX 不会调用相关描述符的__set__方法而是会创建同名的实例属性, **原本的描述符会彻底丢失!**
# 查找顺序(实例上点运算): 数据描述符->实例属性->非数据描述符->类属性   
# 查找顺序(类上点运算): 描述符->类方法    
# 注意不是覆盖顺序!!! 

# In[35]:


# 任何的描述符都可以按如下的方法覆盖掉:

obj = Managed()
Managed.over = 1
Managed.over_no_get = 1
Managed.non_over = 1
# 在 Managed class 的字典里, 同名的
# 描述符全部被覆盖掉了
print(Managed.__dict__)

print(Managed.over, Managed.over_no_get, Managed.non_over)
print(obj.over, obj.over_no_get, obj.non_over)


# ###### Methods are Descriptors
# 
# 实例方法是一个 bound method, 因为它们有 \_\_get\_\_ 方法!!! 因此他们是 非数据描述符

# In[40]:


obj = Managed()
# 注意 在实例上和在class上得到的是不同对象！！！
# As usual with descriptors, 
# the __get__ of a function returns a reference to itself 
# when the access happens **through the managed class**. 
# But when the access goes **through an instance**, 
# the __get__ of the function returns a bound method object: 
# a callable that wraps the function and binds the managed instance 
# (e.g., obj) to the first argument of the function (i.e., self), 
# like the functools.partial function does.
print(obj.spam)
print(Managed.spam)

obj.spam = 7
print(obj.spam)


# In[45]:


# 来看下面的例子

import collections


class Text(collections.UserString):

    def __repr__(self):
        return 'Text({!r})'.format(self.data)

    def reverse(self):
        return self[::-1]


# In[46]:


word = Text('forward')
print(word)
print(word.reverse())
print(Text.reverse(Text('backward')))


# In[47]:


# 这两个调用的返回值: 函数, bounded method
print(type(Text.reverse), type(word.reverse))

# 任何函数(注意不仅仅是实例方法)都是一个非数据描述符,
# 调用它的 __get__ 方法将会得到一个 method bound to that instance
print(Text.reverse.__get__(word))

# 调用 函数对象的 __get__ 方法 并且 instance参数设置为 None 会返回
# 函数本身
print(Text.reverse.__get__(None, Text))

# 等价于 Text.reverse.__get__(word)
print(word.reverse)

# bound method 有一个 __self__ 属性,
# 返回绑定的实例的引用
print(word.reverse.__self__)

# bound method 有一个 __func__ 属性,
# 返回原始函数的引用
print(word.reverse.__func__ is Text.reverse)

# The bound method object also has a __call__ method,
# which handles the actual invo‐cation.
# This method calls the original function referenced in __func__,
# passing the __self__ attribute of the method as the first argument.
# That’s how the implicit binding of the conventional self argument works.


# <center>描述符用法小结</center>
# 
# 1. Use **property** to keep it simple. property 实际上是一个数据描述符. property 也是最简单的定义**只读属性**的方法.
# 2. Read-only descriptors require \_\_set\_\_. 如果你用一个描述符实现了 read-only 的属性, 你需要记得实现 \_\_set\_\_ 和 \_\_get\_\_. 否则同名的赋值语句会覆盖掉描述符. 你的 \_\_set\_\_ 方法可以和 property 中的默认的 \_\_set\_\_ 方法一样抛出 AttributeError.
# 3. validation descriptors can work with \_\_set\_\_ only. 比如上面的例子, validation descriptor 直接继承了父类的 \_\_get\_\_ 而拦截了父类的 \_\_set\_\_
# 4. Caching can be done efficiently with \_\_get\_\_ only. If you code just the \_\_get\_\_ method, you have a nonoverriding descriptor. These are useful to make some expensive computation and then cache the result by setting an attribute by the same name on the instance. The namesake instance attribute will shadow the descriptor, so subsequent access to that attribute will fetch it directly from the instance \_\_dict\_\_ and not trigger the descriptor \_\_get\_\_ anymore.
# 5. Nonspecial methods can be shadowed by instance attributes. Because functions and methods only implement \_\_get\_\_, they do not handle at‐tempts at setting instance attributes with the same name, so a simple assignment like my_obj.the_method = 7 means that further access to the_method through that instance will retrieve the number 7—without affecting the class or other instances. However, this issue does not interfere with special methods. The interpreter only looks for special methods in the class itself, in other words, repr(x) is executed as x.\_\_class\_\_.\_\_repr\_\_(x), so a \_\_repr\_\_ attribute defined in x has no effect on repr(x). For the same reason, the existence of an attribute named \_\_getattr\_\_ in an instance will not subvert the usual attribute access algorithm

# In[ ]:




