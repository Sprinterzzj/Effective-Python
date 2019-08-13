#!/usr/bin/env python
# coding: utf-8

# In[1]:


class OnlyOne(object):
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


# In[ ]:




