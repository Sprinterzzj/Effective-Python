#!/usr/bin/env python
# coding: utf-8

# ###### a decorator factory

# In[2]:


import functools
def statically_typed(*types, return_type=None):
    """statically_type 是一个装饰器工厂, 接受参数并且返回一个装饰器
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            """wrapper 函数只检查位置参数的类型.
            """
            if len(args) > len(types):
                raise ValueError('Too Many Arguments.')
            elif len(args) < len(types):
                raise ValueError('Too Few Arguments.')
            else:
                for i, (arg, arg_type) in enumerate(zip(args, types)):
                    if not isinstance(arg, type_):
                        raise ValueError(f'Arguments {i} must be'
                                         f'of type {type_.__name__}.')
            result = function(*args, **kwargs)
            if (return_type is not None and                not isinstance(result, return_type)):
                raise ValueError(f'Return value must be of type'
                                 f'{return_type.__name__}.')
            else:
                return result
        return wrapper
    return decorator


# ###### class decorators

# In[14]:


import numbers


def ensure(name, validate_func, doc=None):
    """A property factory
    """
    def decorator(cls):
        """为 Cass 增加一个Property, 
        Property 的 setter 方法附有一个 validate function.
        """
        private_name = '__' + name

        def getter(self):
            return getattr(self, private_name)

        def setter(self, value):
            validate_func(name, value)
            setattr(self, private_name, value)
        # 构造Property
        prop = property(fget=getter, fset=setter, doc=doc)
        # 设置Property
        # 注意 setattr 也可以用来设置类属性
        setattr(cls, name, prop)
        return cls
    return decorator

# Some validate function


def is_non_empty_str(name, value):
    if not isinstance(value, str):
        raise ValueError(f'{name} must be of type str.')
    if len(value) == 0:
        raise ValueError(f'{name} should not be empty.')


def is_in_range(minimum=None, maximum=None):
    assert minimum is not None or maximum is not None

    def _is_in_range(name, value):
        if not isinstance(value, numbers.Number):
            raise ValueError(f'{name} must be a number.')
        if minimum is not None and value < minimum:
            raise ValueError(f'{name} {value} is too small.')
        if maximum is not None and value > maximum:
            raise ValueError(f'{name} {value} is too big.')
    return _is_in_range


# In[15]:


@ensure('title', is_non_empty_str)
@ensure('price', is_in_range(1, 1000))
@ensure('quantity', is_in_range(0, 10000))
class Book(object):
    def __init__(self, title, price, quantity):
        self.title = title
        self.price = price
        self.quantity = quantity
    
    @property
    def value(self):
        return self.price * self.quantity


# In[18]:


book = Book('zzj', 450, 1)
print(Book.__dict__)
print(book.__dict__)


# 上面的 stacking decorators 的方式显得比较冗长,
# 有什么方法可以改进?
# 
# 1. 创建两个描述符: NumberField 和 StringField 并且把 validate_func 设置成实例属性
# 2. 创建 Ensure 描述符, 然后用 class decorator

# In[26]:


#下面给出第二种解决方案

class Ensure(object):
    def __init__(self, validate_func, doc=None):
        self.validate_func = validate_func
        self.doc = doc

def do_ensure(cls):
    def make_property(name, attribute):
        private_name = '__' + name
        def getter(self):
            return getattr(self, private_name)
        def setter(self, value):
            attribute.validate_func(name, value)
            setattr(self, private_name, value)
        return property(fget=getter, fset=setter, doc=attribute.doc)
    
    #下面遍历 cls 的类属性
    for name, attribute in cls.__dict__.items():
        if isinstance(attribute, Ensure):
            setattr(cls, name, make_property(name, attribute))
    return cls


@do_ensure
class Book(object):
    title = Ensure(is_non_empty_str)
    price = Ensure(is_in_range(1, 1000))
    quantity = Ensure(is_in_range(0, 10000))
    
    def __init__(self, title, price, quantity):
        self.title = title
        self.price = price
        self.quantity = quantity
    
    @property
    def value(self):
        return self.price * self.quantity


# In[27]:


book = Book('zzj', 450, 1)
print(Book.__dict__)
print(book.__dict__)


# ###### Using a Class Decorator Instead of Subclassing
# 如果父类中的一些非抽象的方法或者属性, 在子类中从来没有更改过, 可以考虑用装饰器

# In[29]:


class Mediated(object):
    def __init__(self):
        self.mediator = None
    def on_change(self):
        if self.mediator is not None:
            self.mediator.on_change(self)

#如果在子类中我们永远不需要重载 on_change 方法, 那么把上面的基类变成装饰器

def Mediated(cls):
    setattr(cls, 'mediator', None)
    def on_change(self):
        if self.mediator is not None:
            self.mediator.on_change(self)
    setattr(cls, 'on_change', on_change)
    return cls


# In[30]:


@Mediated
class A(object):
    pass


# In[31]:


A.__dict__


# In[ ]:




