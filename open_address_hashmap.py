from abc import abstractmethod

from custom_hashmap import CustomHashMap
from hashmap_node import OpenAddressingHashMapNode


class OpenAddressingHashMap(CustomHashMap):
    def __init__(self,max_keys:int=2,threshold_load_factor:int=0.5,resize_factor:int=2,debug:bool=False)->None:
        super().__init__(max_keys,threshold_load_factor,resize_factor,debug)
        self.used_keys_cnt=0
    
    @abstractmethod
    def _get_next_loc(self,node,max_keys:int,attempt:int=1):
        raise NotImplementedError
    
    def _get_node(self,key,value=None):
        return OpenAddressingHashMapNode(key,value)

    def _get_node_loc(self,keys_list:list,max_keys:int,node):
        attempt=0
        key_loc=None
        while key_loc is None or keys_list[key_loc]:
            attempt+=1
            key_loc=self._get_next_loc(node,max_keys,attempt)
            if self.debug:
                print(f"Current Attempt: {attempt} and key_loc: {key_loc}" )
            if keys_list[key_loc] and  keys_list[key_loc].get_key()==node.get_key() and keys_list[key_loc].get_is_deleted()==0:
                break

        return key_loc

    def _insert_node_into_slot(self,keys_list,key_loc,node)->int:
        is_inserted_new_node=False

        if keys_list[key_loc]==None:
            keys_list[key_loc]=node
            is_inserted_new_node=True
        else:
            keys_list[key_loc].set_value(node.get_value())
        return is_inserted_new_node

    def _resize(self):
        if self.debug:
            print(f"resize::Total Keys cnt: {self.keys_cnt} and used keys cnt: {self.used_keys_cnt} Max keys cnt: {self.max_keys}")
        # Step 1: calcualte the new max_keys value via resize_factor
        # Step 2: initialize a new array of new max_keys size with None
        # Step 3: Iterate the last array, 
        #           Iterate the HashMapNode list (if exists)
        #               Calculate a new loc for the key and insert it there 
        
        new_max_keys=self.resize_factor*self.max_keys
        new_keys_list=[None]*new_max_keys

        for node in self.keys_list:
            if node is None:
                continue
            
            if node.get_is_deleted():
                continue

            key_loc=self._get_node_loc(new_keys_list,new_max_keys,node)
            self._insert_node_into_slot(new_keys_list,key_loc,node)

        self.max_keys=new_max_keys
        self.used_keys_cnt=self.keys_cnt
        self.keys_list=new_keys_list
        
        if self.debug:
            print(f"resize:: Resized the Hashmap.\nTotal Keys cnt: {self.keys_cnt} and used keys cnt: {self.used_keys_cnt} Max keys cnt: {self.max_keys}")

    def _get_load_factor(self):
        return self.used_keys_cnt/self.max_keys

    def insert(self,key,value):
        if self.debug:
            print(f"insert:: key: {key} value:{value}")

        node=self._get_node(key,value)
        key_loc=self._get_node_loc(self.keys_list,self.max_keys,node)
        is_a_new_node=self._insert_node_into_slot(self.keys_list,key_loc,node)
        if is_a_new_node:
            self.keys_cnt+=1
            self.used_keys_cnt+=1

        if self._is_resize_needed():
            self._resize()
        
        if self.debug:
            print(f"insert:: Inserted the key: {key}.\nTotal Keys cnt: {self.keys_cnt} and used keys cnt: {self.used_keys_cnt}")
    
    def delete(self,key):
        if self.debug:
            print(f"delete:: key: {key}")
        
        # Step 1: calculate the loc of key
        # Step 2: Iterate on the linked list present on the key
        # Step 3: compare and delete the node with the key
        # Step 4: reduce the key cnt 

        node=self._get_node(key)
        key_loc=self._get_node_loc(self.keys_list,self.max_keys,node)
        
        cur_node=self.keys_list[key_loc]
        if cur_node is None:
            print(f"Key '{key}' does not exist")
            return 
        
        cur_node.set_is_deleted(1)
        self.keys_cnt-=1

        if self.debug:
            print(f"delete:: Deleted the key: {key}.\nTotal Keys cnt: {self.keys_cnt} and used keys cnt: {self.used_keys_cnt}")
        

    def get(self,key):
        if self.debug:
            print(f"get:: key: {key}")

        node=self._get_node(key)
        key_loc=self._get_node_loc(self.keys_list,self.max_keys,node)
        cur_node=self.keys_list[key_loc]

        if cur_node is None:
            print(f"Key '{key}' does not exist")
            return None

        return cur_node.get_value()
    
    def get_meta_data(self):
        print(f"Max keys cnt: {self.max_keys}, Keys cnt: {self.keys_cnt}, Used key cnt: {self.used_keys_cnt}")
        print(f"resize factor: {self.resize_factor} and load factor: {self.threshold_load_factor}")
        for idx in range(self.max_keys):
            print(f"idx: {idx}")
            node=self.keys_list[idx]
            if node is None or node.get_is_deleted():
                continue
            
            print(f"node.key: {node.get_key()} and node.value: {node.get_value()}!")
    


class LinearOpenAddressingHashMap(OpenAddressingHashMap):
    def __init__(self,max_keys:int=2,threshold_load_factor:int=0.5,resize_factor:int=2,debug:bool=False)->None:
        super().__init__(max_keys,threshold_load_factor,resize_factor,debug)

    def _get_next_loc(self,node,max_keys:int,attempt:int=1):
        return (node.get_hash()+attempt)%max_keys
    
class QuadraticOpenAddressingHashMap(LinearOpenAddressingHashMap):

    def __init__(self,max_keys:int=2,threshold_load_factor:int=0.5,resize_factor:int=2,debug:bool=False)->None:
        super().__init__(max_keys,threshold_load_factor,resize_factor,debug)

    def _get_next_loc(self,node,max_keys:int,attempt:int=1):
        return (node.get_hash()+attempt*attempt)%max_keys