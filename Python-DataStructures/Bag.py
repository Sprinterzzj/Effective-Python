from Arrays import Array
from LinkedList import Node, NullNode
from AbstractCollection import AbstractCollection


class Bag(AbstractCollection):
    """Bag is a type of unordered collection.
    实现了 Bag 容器的模板类.
    
    子类需要实现: __init__, __iter__, __str__, clear, 
    add, 以及 remove 方法.
    """
    def __init__(self, sourceCollection=None):
        """子类必须定义自己的`items`实例属性之后,
        再调用 Bag 的初始化函数.
        """
        super().__init__(sourceCollection)
    
    def _isSame(self, other):
        """other 是 另一个长度相同的 Bag 对象
        """
        for item in self:
            if item not in other:
                return False
        return True

    def __contains__(self, item):

        items = getattr(self, 'items', None)
        return item in items

    def clear(self):

        raise NotImplementedError

    def remove(self, item):

        raise NotImplementedError


class ArrayBag(Bag):

    DEFAULT_CAPACITY = 10

    def __init__(self, sourceCollection=None):

        self.items = Array(self.__class__.DEFAULT_CAPACITY)
        super().__init__(sourceCollection)
    
    def __str__(self):
        
        return '{' + ','.join(map(str, self)) + '}'
    
    def __iter__(self):

        for i, item in enumerate(self.items):
            if i == len(self):
                break
            yield item  
    
    def clear(self):
        self.size = 0
        self.items = Array(self.__class__.DEFAULT_CAPACITY)
    
    def _add(self, item):
        """如果数组是否已满, 就先扩容, 然后添加元素到数组末尾
        """
        if len(self) == len(self.items):
            self.items = Array.increase_capacity(self.items)     
        
        self.items[len(self)] = item
    
    def remove(self, item):
        """移除数组中第一个匹配的元素, 移除后有必要就缩容
        """
        if item not in self:
            raise KeyError(f'{item} not in bag.')
   
        for i, _item in enumerate(self):
            if _item == item:
                targetIndex = i
                break   
        # 将 targetIndex及其后的元素左移
        for i in range(targetIndex, len(self) - 1):
            self.items[i] = self.items[i+1]
        
        self.size -= 1
        if len(self) < len(self.items) // 2:
            self.items = Array.decrease_capacity(self.items)


class LinkedBag(Bag):

    def __init__(self, sourceCollection=None):

        self.items = None
        super().__init__(sourceCollection)
    
    def __str__(self):
        return str(self.items)
     
    def __iter__(self):

        return self.items.traversal()
    
    def __contains__(self, item):
        
        return self.items.search(item) != NullNode
  
    def clear(self):
        
        self.size = 0
        self.items = None
    
    def _add(self, item):

        newNode = Node(item, self.items)
        self.items = newNode
    
    def remove(self, item):

        if item not in self:
            raise KeyError(f'{item} not in bag.')
        
        frontNode, targetNode = None, None
        for _item in self:
            if _item.data == item:
                targetNode = _item
                break
            else:
                frontNode = _item
        
        if frontNode is None:
            self.items = self.items.next
        else:
            frontNode.next = targetNode.next
        
        self.size -= 1
        

class ArraySortedBag(ArrayBag):

    def __init__(self, sourceCollection=None):

        super().__init__(sourceCollection)
    
    def _add(self, item):
        
        if len(self) == len(self.items): # 判断数组满了没有, 满了就先扩容
            self._increase_capacity()
        if self.isEmpty() or item >= self.items[len(self) - 1]:
            super()._add(item)
        else:
            for i, _item in enumerate(self):
                if item <= _item:
                    targetIndex = i

            for i in range(len(self), targetIndex, -1):
                self.items[i] = self.items[i - 1]
            
            self.items[targetIndex] = item
    
    def __contains__(self, item):

        left = 0
        right = len(self) - 1
        while left <= right:
            midPoint = (left + right) // 2
            if self.items[midPoint] == item:
                return True
            elif self.items[midPoint] > item:
                right = midPoint - 1
            else:
                left = midPoint + 1
        return False
    
    def _isSame(self, other):
        
        for item1, item2 in zip(self, other):
            if item1 != item2:
                return False
        return True
        






    




    

        
