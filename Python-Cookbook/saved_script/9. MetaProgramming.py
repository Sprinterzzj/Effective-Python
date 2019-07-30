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

# 下面是下一个装饰器, 允许用户提供参数在运行时控制装饰器行为

# In[1]:


from functools import wraps, partial
import logging

# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


# In[3]:


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
            level = newlevel
        
        @attach_wrapper(wrapper)
        def set_msg(newmsg):
            nonlocal logmsg
            logmsg = newmsg
        return wrapper
    print('Return decorate when package the function.')
    return decorate
        


# In[4]:


@logged(logging.DEBUG)
def add(x, y):
    return x + y


# In[5]:





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

# In[31]:


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


# In[33]:


class Spam(object, metaclass=Singleton):
    pass

assert Spam() is Spam()


# In[ ]:




