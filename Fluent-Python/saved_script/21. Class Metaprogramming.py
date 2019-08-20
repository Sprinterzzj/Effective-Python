#!/usr/bin/env python
# coding: utf-8

# If you are not authoring a framework, you should not be writing metaclasses—unless you’re doing it for fun or to practice the con‐cepts.

# ###### A Class Factory

# In[20]:


def record_factory(cls_name, field_names):
    """一个生成类的工厂函数
    """
    try:
        field_names = field_names.replace(',', ' ').split() #1
    except AttributeError:  # no. replace or .split
        pass
    field_names = tuple(field_names) #2

    def __init__(self, *args, **kwargs): #3
        # 按__slots__顺序分配属性的值, 
        # 如果 args 的数目小于 __slots__那么后面多余
        # 的属性不会产生key
        attrs = dict(zip(self.__slots__, args))
        # print(attrs)
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self): #4
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self): #5
        print('self.__slots__: ', self.__slots__)
        
        # self 按照 __slots__ 的顺序初始化, 那么同时迭代
        # __slots__ 和 self 可以得到属性名和相应的值
        values = ', '.join('{}={!r}'.format(*i)
                           for i in zip(self.__slots__, self))
        return f'{self.__class__.__name__}({values})'

    cls_attrs = dict(__slots__=field_names, #6
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__)

    # type(class_name:str, bases:tuple, class_attributs:dict)
    return type(cls_name, (object, ), cls_attrs) #7


# 1. Duck typing in practice: 尝试替换逗号然后分割字符串. 如果失败了, 就默认 `field_name` 是可迭代的, 且非字符串.
# 2. Build a tuple of attribute names. `field_name` 将会赋值给 \_\_slots\_\_.
# 3. 初始化函数
# 4. \_\_iter\_\_ 函数, 按照 \_\_slots\_\_ 的顺序迭代
# 5. \_\_repr\_\_ 函数
# 6. assemble dictionary of class atrributes.
# 7. build and return the new class.

# In[21]:


Dog = record_factory('Dog', 'name weight owner')


# ###### A Class Decorator for Customizing Descriptors

# In[22]:


def entity(cls):
    """类装饰器, 在类定义后被调用, 接受类为唯一的参数.
    遍历class的__dict__, 找到 Validated 的实例(它们是描述符)
    然后更改storage_name属性
    """
    for attr_name, attr_value in cls.__dict__.items():
        if isinstance(attr_value, Validated):
            type_name = type(attr_value).__name__
            attr_value.storage_name = f'__{type_name}_{key}'
        return cls


# ###### A Metaclass for Customizing Descriptors
# Pyhton中所有的类都是 type 的实例, 但是只有元类是 type 的子类

# In[47]:


class Validated(object):
    """我们的Validated descriptor 的代码
    在 19. Dynamic Attributes and Properties.ipynb 里,
    这里弄个假的.
    """
    pass
class EntityMeta(type):
    """Metaclass for business entities with validated fields
    """
    def __init__(cls, class_name, bases, class_dict):
        super().__init__(class_name, bases, class_dict)
        for attr_name, attr in class_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = f'__{type_name}_{attr_name}'

#如果你不想使用metaclass=&&, 那么可以创建一个类然后让LineItem继承它
class Entity(object, metaclass=EntityMeta):
    pass


# ###### The Metaclass __prepare__ Special Method
# Only available in Python 3

# In[3]:


# 元类的 __new__ 和 __init__ 方法接受同样的四个参数.
# class_dict 里面储存了所有的 class attribute.
# 但是, 在 class body 里面的顺序信息就丢失了. Sometimes,
# the order is useful.

#解决方案: __prepare__
# 在metaclass内部 __prepare__ --> __new__ --> __init__


import collections


class Validated(object):
    """我们的Validated descriptor 的代码
    在 19. Dynamic Attributes and Properties.ipynb 里,
    这里弄个假的.
    """
    pass


class EntityMeta(type):
    @classmethod
    def __prepare__(cls, class_name, bases):
        """__prepare__接受三个参数: cls, class_name, bases
        **它必须返回一个mapping**, 这mapping也就是 __new__ 和
        __init__ 的第四个参数.
        """
        return collections.OrderedDict()  # 1

    def __init__(cls, class_name, bases, class_dict):
        super().__init__(class_name, bases, class_dict)
        cls._field_names = []  # 2
        for attr_name, attr in class_dict.items():  # 3
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = f'__{type_name}_{attr_name}'
                cls._field_names.append(attr_name)  # 4


class Entity(object, metaclass=EntityMeta):

    @classmethod
    def field_names(cls): #5
        for name in cls._field_names:
            yield name


# 1. \_\_prepare\_\_ 返回一个空的 OrderedDict 对象, 类对象将(在何时何处?)被储存在这里(好吧, Python 3.7 的默认字典就是保序的...)
# 2. Create a \_field\_names class attribute
# 3. 此处的 class\_dict 是一个 OrderedDict
# 4. 将 Validated 描述符 加入到 \_field\_names 中去
# 5.  生成器函数

# In[ ]:




