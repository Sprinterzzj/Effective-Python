from utils import is_iterable


class AbstractCollection(object):
    """这是所有容器类型的基类
    """

    def __init__(self, sourceCollection=None):
        self.size = 0
        if sourceCollection is not None:
            if not is_iterable(sourceCollection):
                raise TypeError(f'{sourceCollection} is not iterable.')
            for item in sourceCollection:
                self._add(item)
                self.size += 1

    def _add(self, other):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __add__(self, other):
        new_obj = type(self)(self)
        if not is_iterable(other):
            raise TypeError('f{item} is not iterable.')
        for item in other:
            result._add(item)
            self.size += 1
        return result

    def __str__(self):
        for item in self:
            print(item)

    def __len__(self):
        return self.size

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other) or\
           len(self) != len(other):
            return False
        for item1, item2 in zip(self, other):
            if item != item2:
                return False
        return True

    def isEmpty(self):
        return self.size == 0