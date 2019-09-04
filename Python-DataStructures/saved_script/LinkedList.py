#!/usr/bin/env python
# coding: utf-8

# In[1]:


from LinkedList import Node


# In[2]:


# Create a single node
node = Node(0, None)
print(node)


# In[7]:


# create a linked list
head = Node.build(arg_list=list(range(10)))
print(head)


# In[8]:


for nodes in head.traversal():
    print(nodes)


# In[13]:


for i, _ in enumerate(head.traversal()):
    print(head[i])


# In[15]:


newNode = Node(-1, None)
head.insertNode(0, newNode)


# In[ ]:




