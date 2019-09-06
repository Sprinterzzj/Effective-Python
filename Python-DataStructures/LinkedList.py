class Node(object):
    """A single linked node
    """
    def __init__(self, data, next=None):
        
        self.data = data
        self.next = next
    
    @classmethod
    def build(cls, data_list):
        """构造单链表. 尾部节点的 next 为 None.

        Parameters
        ---------
        data_list: a list of data
        """
        if len(data_list) == 0:
            raise ValueError('`data_list`必须至少有一个元素.')
        if len(data_list) == 1:
            head = cls(data_list[0], None)
        else:
            head = cls(data_list[0], cls.build(data_list[1:]))
        return head
    
    def traversal(self):
        """遍历链表
        """
        head = self
        while head is not None:
            yield head
            head = head.next
    
    def search(self, value):
        """顺序遍历链表, 返回 Node.data == value
        的第一个Node, 如果这样的Node不存在就返回NullNode
        """
        for node in self.traversal():
            if node.data == value:
                return node
        return NullNode
    
    def insert(self, index, nodeOrvalue):
        """将`newNode`插入到 index 指定的位置.
        如果 index<0 或 index > 链表总节点数-1, 那么
        抛出 IndexError.
        """
        if not isinstance(nodeOrvalue, self.__class__):
            newNode = self.__class__(nodeOrvalue, None)
        else:
            newNode = nodeOrvalue
            
        if index == 0:
            newNode.next = self
            self = newNode
        else:
            try:
                frontNode = self[index-1]
            except IndexError as e:
                raise IndexError(e)
            else:
                self._insertNode(frontNode, newNode)
        return self
    
    def delete(self, index):
        """index 指定位置的节点删除.
        如果 index<0 或 index > 链表总节点数-1, 那么
        抛出 IndexError.
        """
        if index ==0:
            head = self
            self = self.next
            head.next = None
        else:
            try:
                frontNode = self[index-1]
            except IndexError as e:
                raise IndexError(e)
            else:
                if frontNode.next is not None:
                    targetNode = frontNode.next
                    self._deleteNode(frontNode, targetNode)
        return self
 
    def _insertNode(self, frontNode, newNode):
        """在`frontNode`节点后面插入新的节点
        """
        newNode.next = frontNode.next
        frontNode.next = newNode
    
    def _deleteNode(self, frontNode, targetNode):
        """删除`targetNode`节点
        """
        frontNode.next = targetNode.next
    
    def __getitem__(self, index):
       
        if index <0:
            raise IndexError('`index`必须大于零.')
        for i, node in enumerate(self.traversal()):
            if index == i:
                return node
        raise IndexError(f'链表共有 {i+1} 个节点, `index` 为 {index}.')
    
    def __setitem__(self, index, nodeOrvalue):
        
        if not isinstance(nodeOrvalue, self.__class__):
            newNode = self.__class__(nodeOrvalue, None)
        else:
            newNode = nodeOrvalue    
       
        if index == 0: # 将 `newNode` 替换头部元素
            head = self
            newNode.next = self.next
            self = newNode
            head.next = None
        else:
            try:
                frontNode = self[index-1]
            except IndexError as e:
                raise IndexError(e)
            else:
                if frontNode.next is None: # 将 `newNode` 插入到尾部
                    frontNode.next = newNode
                else: # 替换掉相应位置的节点
                    targetNode = frontNode.next
                    frontNode.next = newNode
                    newNode.next = targetNode.next
 
    def __str__(self):
        
        result = ''
        for i, node in enumerate(self.traversal()):
            result += f'|D{i}:{node.data}|-->'
        result += 'NULL'
        return result
    
NullNode = Node(None, None)