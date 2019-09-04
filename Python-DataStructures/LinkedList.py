class Node(object):
    """A single linked node
    """
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    
    @classmethod
    def build(cls, arg_list):
        if len(arg_list) == 1:
            head = cls(arg_list[0], None)
        else:
            head = cls(arg_list[0], cls.build(arg_list[1:]))
        return head
    
    def traversal(self):
        head = self
        while head is not None:
            yield head
            head = head.next
    
    def searchValue(self, value):
        for node in self.traversal():
            if node.data == value:
                return node
        return NullNode
    
    def searchNode(self, targetNode):
        for node in self.traversal():
            if node is targetNode:
                return node
        return NullNode
    
    def insertNode(self, before, newNode):
        newNode.next = before.next
        before.next = newNode
    
    def deleteNode(self, targetNode):
        if targetNode is None:
            return 
        for node in self.traversal():
            if node.next is targetNode:
                node.next = node.next.next
    
    def __getitem__(self, index):
        if index <0:
            raise IndexError('`index` must be >0.')
        for i, node in enumerate(self.traversal()):
            if index == i:
                return node
        raise IndexError('`index` out of scope.')
    
    def insertIndex(self, index, newNode):
        if index <=0:
            newNode.next = self
        elif index>0:
            try:
                frontNode = self[index-1]
                newNode.next = frontNode.next
                frontNode.next = newNode
            except IndexError:
                pass
    
    def __setitem__(self, index):
        pass
    
    def __str__(self):
        result = ''
        for i, node in enumerate(self.traversal()):
            result += f'|D{i}:{node.data}|-->'
        result += 'NULL'
        return result

NullNode = Node(None, None)