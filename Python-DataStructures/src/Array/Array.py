class Array(object):
    """基于 list 的数组
    """
    def __init__(self, capacity, fillValue=None):
        
        self._items = list()
        for _ in range(capacity):
            self._items.append(fillValue)

    def __len__(self):
        
        return len(self._items)

    def __str__(self):
        
        return str(self._items)

    def __iter__(self):
        
        return iter(self._items)

    def __getitem__(self, index):

        if 0<= index<= len(self) - 1:
            return self._items[index]
        else:
            raise ValueError(f'Index must be >= 0 and <= {len(self)-1}.')

    def __setitem__(self, index, newItem):
        
        if 0<= index<= len(self) - 1:
            self._items[index] = newItem
        else:
            raise ValueError(f'Index must be >= 0 and <= {len(self)-1}.')

    def __contains__(self, item):
        
        return item in self._items
    
    @classmethod
    def increase_capacity(cls, array):
        """`array`必须是`Array`的实例.
        返回一个`array`容量两倍的新数组,
        它按照`array`元素的顺序储存了`array`
        所有的元素.
        """
        if not isinstance(array, cls):
            raise ValueError('`array` must be a instance of Array')

        new_array = cls(len(array) * 2)
        for i, item in enumerate(array):
            new_array[i] = item
        
        return new_array
    
    @classmethod
    def decrease_capacity(cls, array):
        """`array`必须是`Array`的实例.
        返回一个`array`容量1/2的新数组,
        它按照`array`元素的顺序储存了`array`
        一半的元素.
        """
        if not isinstance(array, cls):
            raise ValueError('`array` must be a instance of Array')
        if len(array) < 2:
            raise ValueError('The orginal capacity must be >= 2')
        
        new_array = cls(len(array) // 2)
        for i, item in enumerate(array):
            if i == len(new_array):
                break
            new_array[i] = item


# class Grid(object):
#     """Represents a two-dimensional array.
#     """
#     def __init__(self, rows, columns, fillValue=None):
#         # 每个元素代表了一行
#         self._data = Array(rows)
#         for row in range(rows):
#             self._data[row] = Array(columns, fillValue)
    
#     @property
#     def height(self):
        
#         return len(self._data)
    
#     @property
#     def width(self):
        
#         return len(self._data[0])
    
#     def __getitem__(self, index):
#         """Supports 2-dimensional indexing.
#         """
#         return self._data[index]
    
#     def __str__(self):
        
#         result = ''
#         for row in range(self.height):
#             for col in range(self.width):
#                 result += str(self._data[row][col]) + ' '
#             result += '\n'
#         return result