class Array(object):
    """一般数组(基于list)
    """

    def __init__(self, capacity, fillValue=None):
        self.items = list()
        for i in range(capacity):
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