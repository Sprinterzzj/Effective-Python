#!/usr/bin/env python
# coding: utf-8

# https://realpython.com/async-io-python/
# https://zhuanlan.zhihu.com/p/27258289

# ### asyncio 模块
# 
# 1. 包含各种特定系统实现的模块化事件循环(select等)
# 2. 传输和协议抽象
# 3. 对TCP, UDP, SSL, 子进程, 延时调用以及其他具体的支持
# 4. 模仿dutures模块但是适用于事件循环使用的Future类
# 5. 基于yield from的协议和任务, 可以让你用顺序的方式编写并发代码
# 6. 当我们必须使用一个产生阻塞IO的调用时, 有接口可以把事件转移到线程池
# 7. 模仿threading模块的同步原语, 可以用在单线程内的协程之间

# #### 事件循环 回调(驱动生成器) IO多路复用

# In[ ]:




