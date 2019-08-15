#!/usr/bin/env python
# coding: utf-8

# In[2]:


class ApplicationFramework(object):
    """基类的构造器负责必要的初始化
    """
    def __init__(self):
        self.__templateMethod()

    def __templateMethod(self):
        print('This is a private Template Method.')
        # 我们可以在子类中 override 这些方法.
        self.customize1()
        self.customize2()

    def customize1(self):
        raise NotImplementedError

    def customize2(self):
        raise NotImplementedError


class MyApp(ApplicationFramework):
    """继承了 ApplicationFramework 并且
    override 了 它的实例方法.
    """
    def customize1(self):
        print('This is my customize1.')
    
    def customize2(self):
        print('This is my customize2.')


# In[ ]:




