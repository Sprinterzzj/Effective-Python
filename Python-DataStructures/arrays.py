class Array(object):
    """一般数组(基于list)
    """

    def __init__(self, capacity, fillValue=None):
        
        self.items = list()
        for _ in range(capacity):
            self.items.append(fillValue)

    def __len__(self):
        
        return len(self.items)

    def __str__(self):
        
        return str(self.items)

    def __iter__(self):
        
        return iter(self.items)

    def __getitem__(self, index):
        
        return self.items[index]

    def __setitem__(self, index, newItem):
        
        self.items[index] = newItem
    
    def __contains__(self, item):
        
        return item in self.items
    
    @classmethod
    def increase_capacity(cls, array):
        
        if not isinstance(array, cls):
            raise ValueError('`array` must be a instance of Array')

        new_array = cls(len(array) * 2)
        for i, item in enumerate(array):
            new_array[i] = item
        
        return new_array
    
    @classmethod
    def decrease_capacity(cls, array):

        if not isinstance(array, cls):
            raise ValueError('`array` must be a instance of Array')
        if len(array) < 2:
            raise ValueError('The orginal capacity must be >= 2')
        
        new_array = cls(len(array) // 2)
        for i, item in enumerate(array):
            if i == len(new_array):
                break
            new_array[i] = item


class Grid(object):
    """Represents a two-dimensional array.
    """
    def __init__(self, rows, columns, fillValue=None):
        # 每个元素代表了一行
        self._data = Array(rows)
        for row in range(rows):
            self._data[row] = Array(columns, fillValue)
    
    @property
    def height(self):
        
        return len(self._data)
    
    @property
    def width(self):
        
        return len(self._data[0])
    
    def __getitem__(self, index):
        """Supports 2-dimensional indexing.
        """
        return self._data[index]
    
    def __str__(self):
        
        result = ''
        for row in range(self.height):
            for col in range(self.width):
                result += str(self._data[row][col]) + ' '
            result += '\n'
        return result