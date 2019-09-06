from Arrays import Array
from LinkedList import Node
from AbstractCollection import AbstractCollection


class Stack(AbstractCollection):

    def __init__(self, sourceCollection=None):

        super().__init__(sourceCollection)
      
    def push(self, item):

        self._add(item)
        self.size += 1

    # 下面的实例方法需要在子类中实现
    def _add(self, item):

        raise NotImplementedError

    def peek(self):

        raise NotImplementedError

    def pop(self):

        raise NotImplementedError

    def clear(self):

        raise NotImplementedError


class ArrayStack(Stack):

    DEFAULT_CAPACITY = 10

    def __init__(self, sourceCollection=None):

        self.items = Array(self.__class__.DEFAULT_CAPACITY)
        super().__init__(sourceCollection)
    
    def __iter__(self):

        for i, item in enumerate(self.items):
            if i == len(self):
                break
            yield item 
    
    def _add(self, item):

        if len(self) == len(self.items):
            self.items = Array.increase_capacity(self.items)
        self.items[len(self)] = item
    
    def peek(self):
        
        if self.isEmpty():
            raise KeyError('The stack is empty.')
        return self.items[len(self) - 1]
    
    def pop(self):

        if self.isEmpty():
            raise KeyError('The stack is empty.')
        topItem = self.items[len(self) - 1]
        
        self.size -= 1
        if len(self) < len(self.items) // 2:
            self.items = Array.decrease_capacity(self.items)

        return topItem
    
    def clear(self):

        self.size = 0
        self.items = Array(self.__class__.DEFAULT_CAPACITY)
        

    
