from arrays import Array

class Grid(object):
    """Represents a two-dimensional array.
    """
    def __init__(self, rows, columns, fillValue=None):
        # 每个元素代表了一行
        self._data = Array(rows)
        for row in range(rows):
            self.data[row] = Array(columns, fillValue)
    
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
                result += str(self.data[row][col]) + ' '
            result += '\n'
        return result
    
