#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#函数对象是如何运行的" data-toc-modified-id="函数对象是如何运行的-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>函数对象是如何运行的</a></span><ul class="toc-item"><li><span><a href="#在函数调用时,-首先用PyEval_EvalFramEx(C-函数)来执行-foo函数" data-toc-modified-id="在函数调用时,-首先用PyEval_EvalFramEx(C-函数)来执行-foo函数-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>在函数调用时, 首先用PyEval_EvalFramEx(C 函数)来执行 foo函数</a></span></li><li><span><a href="#PyEval_EvalFramEx会创建-PyFrameObject(栈帧对象):" data-toc-modified-id="PyEval_EvalFramEx会创建-PyFrameObject(栈帧对象):-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>PyEval_EvalFramEx会创建 PyFrameObject(栈帧对象):</a></span></li></ul></li></ul></div>

# ##### 函数对象是如何运行的

# In[1]:


import inspect
import dis


# In[2]:


def foo():
    bar()
def bar():
    a = 3
    return a


# ###### 在函数调用时, 首先用PyEval_EvalFramEx(C 函数)来执行 foo函数

# ###### PyEval_EvalFramEx会创建 PyFrameObject(栈帧对象):
# 1. 栈帧是分配在堆上的, 所以在函数调用结束后不会主动释放
# 2. PyFrameObject有两个属性: f\_back 和 f\_code. 后者指向了当前函数的字节码对象(PyCodeObject), 前者指向了调用该函数的栈帧对象的f_code.

# In[5]:


#首先用diss.diss模块来查看函数的字节码

#函数调用是递归的
dis.dis(foo)


# In[6]:


dis.dis(bar)


# In[7]:


#我们可以获取函数的栈帧对象
frame = None
def foo():
    bar()
def bar():
    global frame
    a = 2
    frame = inspect.currentframe()


# In[ ]:




