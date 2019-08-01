#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#数组实现" data-toc-modified-id="数组实现-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>数组实现</a></span></li><li><span><a href="#应用:-括号匹配" data-toc-modified-id="应用:-括号匹配-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>应用: 括号匹配</a></span></li><li><span><a href="#算数表达式" data-toc-modified-id="算数表达式-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>算数表达式</a></span></li></ul></div>

# In[3]:


from AbstractCollection import AbstractCollection


class AbstractStack(AbstractCollection):
    """抽象Stack类
    """

    def __init__(self, sourcecollection=None):
        super().__init__(sourcecollection)

    def _add(self, item):
        self.push(item)


# In[10]:





# ###### 数组实现

# In[9]:



class ArrayStack(AbstractStack):
    _DEFAULT_CAPACITY = 10


# In[ ]:


def test(stackType): # Test any implementation with the same code 
    s = stackType() 
    print("Length:", len(s)) 
    print("Empty:", s.isEmpty()) 
    print("Push 1-10") 
    for i in range(10): 
        s.push(i + 1) 
    print("Peeking:", s.peek()) 
    print("Items (bottom to top):", s) 
    print("Length:", len(s)) 
    print("Empty:", s.isEmpty()) 
    theClone = stackType(s) 
    print("Items in clone (bottom to top):", theClone) theClone.clear() print("Length of clone after clear:", len(theClone)) print("Push 11") s.push(11) print("Popping items (top to bottom):", end="") while not s.isEmpty(): print(s.pop(), end=" ") print("\nLength:", len(s)) print("Empty:", s.isEmpty())


# ######  应用: 括号匹配

# In[47]:


def brackets_balance(exp):
    """exp 是字符串, 代表着一个表达式.
    """
    stack = LinkedStack()
    if len(exp) == 0: return True
    for e in exp:
        if e in ('(', '['):
            stack.push(e)
        elif e in (')', '}'):
            if stack.isEmpty():
                return False
            elif (stack.peek() != '(' and e == ')') or                 (stack.peek() != '[' and e == ']'):
                return False
            else:
                stack.pop()
    return stac.isEmpty()


# In[46]:


# brackets_balance('(...)...(...)')
# brackets_balance('(...)...(...')
# brackets_balance(')...(...(...)')
# brackets_balance('[...(...)...]')
# brackets_balance('[...(...]...]')


# ###### 算数表达式

# In[ ]:




