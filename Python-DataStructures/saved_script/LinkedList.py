#!/usr/bin/env python
# coding: utf-8

# In[49]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[59]:


from LinkedList import Node


# In[60]:


# 构造单个节点
node = Node(0, None)
print(node)


# In[61]:


# 构造链表
head = Node.build(data_list=[1,2,3,4,5])
print(head)


# In[62]:


# 遍历链表
for nodes in head.traversal():
    print(nodes)


# In[63]:


# getitem
for i, _ in enumerate(head.traversal()):
    print(head[i])


# In[64]:


# setitem
newNode0 = Node(-1, None)
newNode3 = Node(-1, None)
newNode5 = Node(-1, None)


# In[65]:


head[0] = newNode0
print(head)
print(newNode0)


# In[66]:


# 替换第四个节点
head = newNode0
head[3] = newNode3
print(head)


# In[67]:


# 插入到末尾
head[5] = newNode5
print(head)


# In[70]:


# 删除头部节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.delete(0)
print(head)
print(newHead)


# In[71]:


# 删除尾部节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.delete(4)
print(head)
print(newHead)


# In[72]:


# 删除中间节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.delete(3)
print(head)
print(newHead)


# In[73]:


# 插入头部节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.insert(0, Node(-1, None))
print(head)
print(newHead)


# In[74]:


# 插入中间节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.insert(4, Node(-1, None))
print(head)
print(newHead)


# In[75]:


# 插入尾部节点
head = Node.build(data_list=[1,2,3,4,5])
print(head)
newHead = head.insert(5, Node(-1, None))
print(head)
print(newHead)


# In[ ]:




