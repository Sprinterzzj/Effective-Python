#!/usr/bin/env python
# coding: utf-8

# 1. 属性描述符本质上是**类方法**.
# 2. 和 property 一样. 实例的点运算操作会优先 access 描述符.

# In[12]:


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


# In[16]:


x = LineItem('zzj', 90, 450)
print(x.__dict__)
print(x.weight)


# In[23]:


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


# In[24]:


x = LineItem('zzj', 90, 450)
print(x.__dict__)
print(x.weight)
print(Quantity.counter())


# In[ ]:




