#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#让我们仔细的看一看" data-toc-modified-id="让我们仔细的看一看-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>让我们仔细的看一看</a></span></li><li><span><a href="#问题出现了!!!!" data-toc-modified-id="问题出现了!!!!-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>问题出现了!!!!</a></span></li><li><span><a href="#为了方便理解,-我们把函数改成" data-toc-modified-id="为了方便理解,-我们把函数改成-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>为了方便理解, 我们把函数改成</a></span></li><li><span><a href="#解决方案" data-toc-modified-id="解决方案-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>解决方案</a></span></li><li><span><a href="#一个小例子" data-toc-modified-id="一个小例子-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>一个小例子</a></span></li></ul></div>

# In[1]:


#首先定义如下的闭包函数
def mul_func_gen(max):
    for i in range(max):
        yield lambda x: x*i


# In[6]:


mul_func = mul_func_gen(3)

#0, 3, 6
print([f(3) for f in mul_func])


# In[7]:


mul_func = list(mul_func_gen(3))

#6, 6, 6
print([f(3) for f in mul_func])


# ###### 让我们仔细的看一看

# In[8]:


mul_func = mul_func_gen(3)


# In[9]:


mul_func


# In[10]:


mul_1 = next(mul_func)


# In[11]:


mul_1


# In[13]:


cell_1 = mul_1.__closure__[0]


# In[15]:


cell_1.cell_contents


# In[16]:


mul_2 = next(mul_func)
cell_2 = mul_2.__closure__[0]
cell_2.cell_contents


# ###### 问题出现了!!!!

# In[17]:


#变成了1
cell_1.cell_contents


# In[18]:


#延迟绑定: 调用了 next方法后 cell_1的 content也会跟着变
cell_1 is cell_2


# ###### 为了方便理解, 我们把函数改成
# 简单来说，在python里，相对而言的局部变量绑定的是值，非局部变量绑定的是空间， 而不是值本身，所以，for循环生成的i，相对于函数lam来说，是全局变量，所以绑定的是i所在的内存地址，但i最后变成了3，lam绑定的是3。

# In[20]:


def mul():
    res_list = []
    for i in range(4):
        def lam(x):
            return x * i
        res_list.append(lam)
    return res_list


# In[ ]:





# ###### 解决方案

# In[ ]:


def mul_func_gen(max):
    for i in range(max):
        #在函数定义的时候赋值参数
        yield lambda x, i = i: x * i


# ###### 一个小例子

# In[19]:


from contextlib import contextmanager
from time import perf_counter


# In[ ]:


@contextmanager
def timing(label):
    t0 = perf_counter()
    yield lambda : (t1 - t0)
    t1 = perf_counter()

