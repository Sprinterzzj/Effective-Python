from Arrays import Array
from LinkedList import Node
from AbstractCollection import AbstractCollection


class Stack(AbstractCollection):
    """ Stack 的模板类. 定义了 Stack 的方法.
    Stack 的子类需要实现以下方法:
    1. _add
    2. __iter__
    3. peek
    4. pop
    5. clear
    """

    def __init__(self, sourceCollection=None):
        """初始化函数. 将 sourceCollection 的元素添加到
        `items`属性中, `items` 属性储存了 Stack 的元素.
        注意: Stack 的子类必须在 __init__中首先定义
        `items`属性, 然后调用 Stack 的 __init__.
        """

        super().__init__(sourceCollection)
      
    def push(self, item):
        """将元素压到栈顶.
        """
        self._add(item)
        self.size += 1

    # 下面的实例方法需要在子类中实现
    def _add(self, item):
        """向栈顶添加元素的底层函数.
        注意: 在这个函数中 `size` 属性
        无需递增.
        """
        raise NotImplementedError

    def peek(self):
        """返回栈顶元素的值.
        如果栈为空, 就抛出 KeyError 异常.
        """
        raise NotImplementedError

    def pop(self):
        """返回栈顶元素的值, 删除栈顶元素,
        `size` 递减.
        如果栈为空, 就抛出 KeyError 异常.
        """
        raise NotImplementedError

    def clear(self):
        """清空 Stack所有的元素.
        """
        raise NotImplementedError


class ArrayStack(Stack):
    """用数组实现了栈的类.
    """

    DEFAULT_CAPACITY = 10

    def __init__(self, sourceCollection=None):
        """初始化函数. `items` 属性储存了栈的元素,
        它是一个 `Array`的实例, 其第一个元素是栈底元素.
        """
        self.items = Array(self.__class__.DEFAULT_CAPACITY)
        super().__init__(sourceCollection)
    
    def __iter__(self):
        """返回从栈底到栈顶元素的 view.
        """
        for i, item in enumerate(self.items):
            if i == len(self):
                break
            yield item 
    
    def _add(self, item):
        """首先判断 `items` 是否需要扩容, 如果需要
        就先扩容, 然后将 `item` 加入到栈顶.
        """
        if len(self) == len(self.items):
            self.items = self.items.__class__.increase_capacity(self.items)
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
            self.items = self.items.__class__.decrease_capacity(self.items)

        return topItem
    
    def clear(self):

        self.size = 0
        self.items = Array(self.__class__.DEFAULT_CAPACITY)


class LinkedStack(Stack):
    """用链表实现了栈的类.
    """

    def __init__(self, sourceCollection=None):
        """初始化函数. `items` 是一个 `Node`的实例, 
        它永远是储存了栈顶元素的节点.
        """
        self.items = None
        super().__init__(sourceCollection)
    
    def __iter__(self):
        
        def viewNodes(node):
            if node.next is None:
                return node.data
            else:
                return viewNodes(node.next)
        
        if self.items is None:
            return None:
        else:
            return iter(viewNodes(self.items))
    
    def _add(self, item):
        """判断 item 是否为 `Node`的实例, 如果不是就
        创建一个新的 Node, 它的 `data`属性储存了`item`. 
        然后将 Node.next 指向当前的 `items`, 最后
        将这个新节点赋值给 `items`.
        """
        if not isinstance(item, self.items.__class__):
            item = self.items.__class__(item, self.items)
        else:
            item.next = self.items
        
        self.items = item
    
    def peek(self):
        """
        returns
        -------
        栈顶元素的值(不是`Node`的实例)
        """
        if self.isEmpty():
            raise KeyError('The stack is empty.')
        return self.items.data
    
    def pop(self):
        """
        returns
        -------
        栈顶元素的值(不是`Node`的实例)
        """
        if self.isEmpty():
            raise KeyError('The stack is empty.')
        oldItem = self.items.data
        self.items = self.items.next
        self.size -= 1
        return oldItem
    
    def clear(self):

        self.size = 0
        self.items = None

        

    
