from collections.abc import Iterable


class AbstractCollection(object):
    """这是所有容器类型的基类
    实现了如下的默认方法:
    __add__, __str__, __len__, isEmpty,
    子类可以继承或者重载它们;
    
    下面的方法需要子类自己实现:
    _add, __iter__, _isSame
    


    __eq__ 函数只做了基本的检查, 子类应该在调用它之后
    完成剩余的判断逻辑.
    """

    def __init__(self, sourceCollection:Iterable=None):
        """初始化函数. 将可迭代对象`sourceCollection`的值
        依次添加到容器内. 子类必须在 __init__ 内部定义
        `items`属性再调用 `AbstractCollection`类的初始化函数,
        否则会抛出 AttributeError 异常.
        """      
        if not hasattr(self, 'items'):
            raise AttributeError('`items` attribute is not defined.')
        
        self.size = 0
        if sourceCollection is not None:
            if not isinstance(sourceCollection, Iterable):
                raise TypeError(f'{sourceCollection} is not iterable.')
            for item in sourceCollection:
                self._add(item)
                self.size += 1

    def _add(self, item):
        """向容器添加元素的底层函数,
        完成添加元素的具体操作.
        """
        raise NotImplementedError

    def __iter__(self):
        
        raise NotImplementedError

    def __add__(self, other:Iterable):
        """接受一个可迭代对象`other`,
        将它的元素依次添加到当前容器的
        一个副本中, 返回这个副本.
        """
        result = self.__class__(self)
        if not isinstance(other, Iterable):
            raise TypeError(f'{other} is not iterable.')
        for item in other:
            result._add(item)
            self.size += 1
        return result

    def __str__(self):
        """逐次打印容器中的元素
        """
        for item in self:
            print(item)

    def __len__(self):
        
        return self.size

    def __eq__(self, other):
        """__eq__ 函数只做基本的判断:
        首先判断 两个对象是否相同, 如果
        相同返回 True.
        如果两个对象不同, 判断两个对象的类型和长度,
        二者有一个不等就返回 False, 否则调用
        isSame 函数.
        """
        if self is other:
            return True
        
        if type(self) != type(other) or\
           len(self) != len(other):
           return False
        
        return self._isSame(other)

    def isEmpty(self):
        
        return self.size == 0
    
    def _isSame(self, other):
        """判断两个长度相等类型相同
        的容器是否相等的底层函数.
        """
        raise NotImplementedError