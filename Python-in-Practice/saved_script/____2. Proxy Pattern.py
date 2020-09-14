#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#代理模式:-一个简单的例子" data-toc-modified-id="代理模式:-一个简单的例子-0.0.1"><span class="toc-item-num">0.0.1&nbsp;&nbsp;</span>代理模式: 一个简单的例子</a></span></li></ul></li></ul></li><li><span><a href="#Proxy-Pattern" data-toc-modified-id="Proxy-Pattern-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Proxy Pattern</a></span></li></ul></div>

# ###### 代理模式: 一个简单的例子
# 
# 有常见的四种代理类型:
# 
# 1. A remote proxy.使得访问远程对象就像本地访问一样，例如网络服务器。隐藏复杂性，使得访问本地远程统一。比如ORM
# 2. A virtual proxy。用来实现延迟访问，比如一些需要复杂计算的对象，python里可以实现lazy_property，性能改善
# 3. A protection/protective proxy. 控制敏感对象的访问，加上一层保护层，实现安全控制
# 4. A smart(reference) proxy. 访问对象时加上一层额外操作，例如引用计数和线程安全检查。weakref.proxy()

# In[4]:


# 是用描述符实现 Lazy Property

class LazyProperty(object):
    """用描述符实现延迟加载的属性
    """
    def __init__(self, method):
        
        self.method = method
        self.method_name = method.__name__
    
    def __get__(self, instance, instance_type):
        
        if instance is None:    
            return None
        value = self.method(instance)
        print(f'value : {value}')
        setattr(instance, self.method_name, value) # 在第一次调用 __get__ 方法时会调用 method, 然后设置属性
        return value
    
class Test(object):
        
    def __init__(self):
            
        self.x = 'foo'
        self.y = 'bar'
        self._resource = None
        
    @LazyProperty
    def resource(self):
        print(f'Initializing self._resource which is : {self._resource}.')
        self._resource = tuple(range(10))
        return self._resource
        


# In[5]:


t = Test()
print(t.resource)
print(t.resource)


# In[6]:


t.__dict__


# In[8]:


# 用代理实现安全控制

class SensitiveInfo(object):
    
    def __init__(self):
        
        self.users = ['nick', 'tom', 'ben', 'mike']
    
    def read(self):
        
        print('There are {} users : {}.'
              .format(len(self.users), ' '.join(self.users)))
    
    def add(self, user):
        
        self.users.append(user)
        print('Added user {}'.format(user))


class Info(object):
    """Protection proxy to SensitiveInfo
    """
    def __init__(self):
        
        self.protected = SensitiveInfo()
        # 为了方便展示, 这里直接把安全密钥写在代码里, 为了安全不应该这么做
        self.secret = '123'
    
    def read(self):
        
        self.protected.read()
    
    def add(self, user):
        """给 add 操作加上秘钥验证, 保护 add 操作
        """
        sec = input('What is the secret ?')
        self.protected.add(user) if sec == self.secret else print('That is wrong.')


# 上面这个示例有几个缺点:
# 
# 1. SensitiveInfo可以被直接实例化使用，绕过Info类，可以考虑使用abc模块避免SensitiveInfo被直接实例化 
# 2. 密钥直接写死在代码里，应该用安全性较高密钥写到配置或者环境变量里

# #### Proxy Pattern

# In[ ]:





# In[ ]:




