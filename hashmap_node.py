import mmh3

class HashMapNode:
    def __init__(self,key,value=None,next:'HashMapNode'=None)->None:
        self._key=key
        self._value=value
        self._next=next
        self._hash=hash(key)

    def get_key(self):
        return self._key
    
    def get_value(self):
        return self._value
    
    def get_next(self):
        return self._next

    def get_hash(self):
        return self._hash
    
    def set_value(self,value):
        self.value=value

    def set_next(self,next):
        self._next=next
        
class OpenAddressingHashMapNode(HashMapNode):
    def __init__(self,key,value=None,next:'OpenAddressingHashMapNode'=None)->None:
        super().__init__(key,value,next)
        self._is_deleted=0

    def get_is_deleted(self):
        return self._is_deleted

    def set_is_deleted(self,is_deleted:int=0):
        self._is_deleted=is_deleted

class OpenAddressingDoubleHashMapNode(HashMapNode):
    def __init__(self,key,value=None,next:'OpenAddressingHashMapNode'=None)->None:
        super().__init__(key,value,next)
        self._is_deleted=0
        self._hash2=mmh3.hash(key)

    def get_is_deleted(self):
        return self._is_deleted

    def get_hash2(self):
        return self._hash2

    def set_is_deleted(self,is_deleted:int=0):
        self._is_deleted=is_deleted

    