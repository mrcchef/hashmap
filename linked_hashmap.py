from custom_hashmap import CustomHashMap
from hashmap_node import HashMapNode


class LinkedListHashMap(CustomHashMap):
    def __init__(self,max_keys:int=2,threshold_load_factor:int=0.5,resize_factor:int=2,debug:bool=False)->None:
        super().__init__(max_keys,threshold_load_factor,resize_factor,debug)
    
    def _get_node_loc(self,max_keys:int,node:HashMapNode):
        return node.get_hash()%max_keys
    
    def _get_node(self,key,value=None):
        return HashMapNode(key,value)
    
    def _insert_node_into_slot(self,keys_list:list[HashMapNode],key_loc:int,node:HashMapNode)->int:
        is_inserted_new_node=False

        # If key_loc has empty linked list
        if keys_list[key_loc]==None:
            keys_list[key_loc]=node
            is_inserted_new_node=True
        else:
            # Iterate through the list and if already exist update the new value
            cur_node=keys_list[key_loc]
            prev_node=None
            while cur_node:
                if cur_node.get_key()==node.get_key():
                    cur_node.set_value(node.get_value())
                    break
                prev_node=cur_node
                cur_node=cur_node.get_next()

            # If not present, insert at the end
            if cur_node==None:
                prev_node.set_next(node)
                is_inserted_new_node=True
        
        return is_inserted_new_node
    
    def insert(self,key,value):
        if self.debug:
            print(f"insert:: key: {key} value:{value}")
        # Step 1: I need to get the loc of key in keys_list
        # Step 2: Insert the node in the key_loc
        # Step 3: check the current load factor with threashold load factor
        #           If load_factor>=threashold load factor then resize the keys list

        node=self._get_node(key,value)
        key_loc=self._get_node_loc(self.max_keys,node)
        
        is_a_new_node=self._insert_node_into_slot(self.keys_list,key_loc,node)
        if is_a_new_node:
            self.keys_cnt+=1

        if self._is_resize_needed():
            self._resize()

    def _resize(self):
        if self.debug:
            print(f"resize::Total Keys cnt: {self.keys_cnt} and Max keys cnt: {self.max_keys}")
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
            
            while node:
                new_node=self._get_node(node.get_key(),node.get_value())
                key_loc=self._get_node_loc(new_max_keys,new_node)
                self._insert_node_into_slot(new_keys_list,key_loc,new_node)
                node=node.get_next()

        self.max_keys=new_max_keys
        self.keys_list=new_keys_list
        if self.debug:
            print("Resized the Hashmap")
            print(f"Now max_keys: {self.max_keys}")
    
    def delete(self,key):
        if self.debug:
            print(f"delete:: key: {key}")
        # Step 1: calculate the loc of key
        # Step 2: Iterate on the linked list present on the key
        # Step 3: compare and delete the node with the key
        # Step 4: reduce the key cnt 

        node=self._get_node(key)
        key_loc=self._get_node_loc(self.max_keys,node)
        
        cur_node=self.keys_list[key_loc]
        if cur_node is None:
            print(f"Key '{key}' does not exist")
            return 
        elif cur_node.get_key()==key:
            self.keys_list[key_loc]=cur_node.get_next()
            self.keys_cnt-=1
            return 
        
        prev_node=None
        while cur_node:
            if cur_node.get_key()==key:
                prev_node.set_next(cur_node.get_next())
                self.keys_cnt-=1
                break
            prev_node=cur_node
            cur_node=cur_node.get_next()

    def get(self,key):
        node=self._get_node(key)
        key_loc=self._get_node_loc(self.max_keys,node)
        cur_node=self.keys_list[key_loc]

        if cur_node is None:
            print(f"Key '{key}' does not exist")
            return None

        while cur_node:
            if cur_node.get_key()==key:
                return cur_node.get_value()
            cur_node=cur_node.get_next()

        return None
    
    def get_meta_data(self):
        print(f"Max keys cnt: {self.max_keys}, Keys cnt: {self.keys_cnt}")
        print(f"resize factor: {self.resize_factor} and load factor: {self.threshold_load_factor}")
        
        for idx in range(self.max_keys):
            print(f"idx: {idx}")

            node_cnt=0
            node=self.keys_list[idx]

            while node:
                node_cnt+=1
                print(f"node.key: {node.get_key()} and node.value: {node.get_value()}!")
                node=node.get_next()
            
            print(f"Total nodes are: {node_cnt}")

    def __name__(self):
        return 'LinkedListHashMap'
