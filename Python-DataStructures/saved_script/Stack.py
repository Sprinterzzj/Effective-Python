#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#应用:-括号匹配" data-toc-modified-id="应用:-括号匹配-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>应用: 括号匹配</a></span></li><li><span><a href="#算数表达式" data-toc-modified-id="算数表达式-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>算数表达式</a></span></li></ul></div>

# In[48]:


class LinkedStack(object):
    def __init__(self, items=None):
        if items_ is None:
            self._list = []
        elif isinstance(items_, LinkedStack):
            self._list = 
        else:
            self._list = list(list_)

    def __len__(self):
        return len(self._list)

    def isEmpty(self):
        if self.__len__() == 0:
            return True
        else:
            return False

    def __str__(self):
        return str(self._list)

    def __iter__(self):
        return (s for s in self._list)

    def __contains__(self, item):
        return item in self._list

    def __add__(self, s):
        if isinstance(s, LinkedStack):
            return LinkedStack(self._list + s._list)

    def __eq__(self, s):
        if not isinstance(s, LinkedStack):
            return False
        if not self.__len__() == len(s):
            return False
        for e1, e2 in zip(self, s):
            if e1 != e2:
                return False
        return True

    def clear(self):
        self._list = []

    def peek(self):
        if self.isEmpty():
            raise KeyError
        return self._list[-1]

    def push(self, item):
        self._list.append(item)

    def pop(self):
        if self.isEmpty():
            raise KeyError
        return self._list.pop()


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


# In[22]:


# 使用:

# s = LinkedStack()
# s.push(1)
# s.push(2)
# s.push(3)
# s.isEmpty()
# len(s)
# s.peek()
# s.pop()
# s.pop()
# s.pop()
# s.peek()
# s.pop()
# s.push(4)
# str(s)


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




