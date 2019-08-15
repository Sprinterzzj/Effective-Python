#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 第一个实现
class OnlyOne(object):
    """你可以创建多个 OnlyOne 的实例,
    但是内部的 __OnlyOne 实例是唯一的.
    """
    class __OnlyOne(object):
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if OnlyOne.instance is None:
            # 第一次初始化时, 将新的 __OnlyOne 实例赋值给
            # instance.
            OnlyOne.instance = OnlyOne.__OnlyOne(arg)
        else:
            # 如果 instance 已经存在, 那么更新其 val 属性
            OnlyOne.instance.val = arg
    # 重定向 getattr 接口
    def __getattr__(self, name):
        return getattr(self.instance, name)


# In[9]:


# 第二个实现
class OnlyOne(object):
    class __OnlyOne(object):
        def __init__(self):
            self.val = None

        def __str__(self):
            return 'self : ' + str(self.val)
    instance = None
    # new 方法永远是一个类方法
    def __new__(cls):
        """new 方法控制实例的构造; init 控制实例的初始化.
        如果 new 方法 发现 instance 已经存在了, 就跳过构造
        过程.
        """
        if not cls.instance:
            cls.instance = cls.__OnlyOne()
        return cls.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)


# In[15]:


x = OnlyOne()
y = OnlyOne()
assert x is y, 'Fuck no!'


# In[17]:


# 第三个实现
class Borg(object):
    """Borg class 的效果与上面两个实现相同, 但是
    """
    _share_dict = {}

    def __init__(self):
        """Borg 的子类初始化时, 共享相同的 __dict__
        """
        self.__dict__ = self._share_dict


class Singleton(Borg):
    def __init__(self, arg):
        super().__init__()
        # 等价于 self.__dict__.update({'val':arg})
        self.val = arg

    def __str__(self):
        return self.val


# In[19]:


x = Singleton(123)
y = Singleton(233)
print(x is y)
print(x.val)


# In[21]:


# 第四个实现
class SingleTone(object):
    __instance = None

    def __new__(cls, val):
        """SingleTone 的子类在创建实例时会调用之;
        但是子类的参数在此处被初始化.
        """
        if SingleTone.__instance is None:
            SingleTone.__instance = super().__new__(cls)
        SingleTone.__instance.val = val
        return SingleTone.__instance


class Singleton(SingleTone):
    def __init__(self, arg):
        pass


# In[25]:


x = Singleton(2)
y = Singleton(3)
x is y


# In[27]:


# 第五个实现
class SingletonDecorator(object):
    def __init__(self, kclass):
        self.kclass = kclass
        self.instance = None
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.isinsace = self.kclass(*args, **kwargs)
        return self.instance


# In[28]:


@SingletonDecorator
class foo(object):
    pass


# In[29]:


x = foo()
y = foo()
x is y


# In[ ]:


# 第六个实现
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


# In[42]:


# 第七个实现
class Singleton(type):
    def __init__(cls, class_name, bases, class_dict):
        print('call metaclass\'s init')
        super().__init__(class_name, bases, class_dict)
        original_new = cls.__new__
        def my_new(cls, *args, **kwargs):
            print('call new before init')
            if cls.instance is None:
                cls.instance = original_new(cls)
            return cls.instance
        cls.instance = None
        cls.__new__ = my_new

class bar(object, metaclass=Singleton):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return 'self : ' + str(val)
    


# In[43]:


a = bar(3)
b= bar(4)
a is b


# <center>使用场景</center>
# 
# 1.所有对象共同享有相同的 state/data.

# In[ ]:




