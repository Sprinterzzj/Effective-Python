class Bag(object):
    """Bag is a type of unordered collection.
    实现了 Bag 容器的模板类
    """
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which
        includes the contents of sourceCollection, if it's
        present.
        """
        raise NotImplementedError

    def isEmpty(self):
        
        return len(self) == 0
    
    def __len__(self):
        
        raise NotImplementedError

    def __str__(self):

        raise NotImplementedError

    def __iter__(self):

        raise NotImplementedError

    def __add__(self, other):
        
        raise NotImplementedError

    def __eq__(self, other):
        
        raise NotImplementedError

    def clear(self):
        pass

    def add(self, item):
        pass

    def remove(self, item):
        pass


from Arrays import Array

class ArrayBag(Bag):

    DEFAULT_CAPACITY = 10

    def __init__(self, sourceCollection=None):

        self.items = Array(self.__class__.DEFAULT_CAPACITY)
        self.size = 0
        if sourceCollection is not None:
            for item in sourceCollection:
                self.add(item)
    
    def __len__(self):
        
        return self.size
    
    def __str__(self):
        
        return '{' + ','.join(map(str, self)) + '}'
    
    def __iter__(self):

        for item in self.items:
            yield item
    
    def __add__(self, other):

        result = self.__class__
