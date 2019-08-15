#!/usr/bin/env python
# coding: utf-8

# 代理
# 
# 代理模式 用来**控制 implementation 的访问**.

# In[ ]:


# Simple demonstration of the Proxy pattern


class Implementation(object):
    def f(self):
        print('***f***')
        return

    def g(self):
        print('***g***')
        return

    def h(self):
        print('***h***')
        return

class Proxy(object):
    def __init__(self):
        self.__implementation = Implementation()
    
    # Pass method calls to the implementation
    def f(self):
        self.__implementation.f()
    def g(self):
        self.__implementation.g()
    def h(self):
        self.__implementation.h()


# In[3]:


# 当然我们可以用 Python 的特性

class Implementation(object):
    def f(self):
        print('***f***')
        return

class Proxy(object):
    def __init__(self):
        self.__implementation = Implementation()
    def __getattr__(self, name):
        """重定向 __getattr__ 方法
        """
        return getattr(self.__implementation, name)


# State
# 
# State pattern adds more implementations to Proxy. State 模式可以切换 Implementation 的种类

# In[4]:


class State_d(object):
    def __init__(self, imp):
        self.__implementation = imp
    def changeImp(self, newImp):
        self.__implementation = newImp
    
    def __getattr__(self, name):
        return getattr(self.__implementation, name)


# In[ ]:




