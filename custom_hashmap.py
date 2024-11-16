from abc import ABC, abstractmethod

class CustomHashMap(ABC):
    def __init__(self,max_keys:int=2,threshold_load_factor:int=0.5,resize_factor:int=2,debug:bool=False)->None:
        self.max_keys=max_keys
        self.keys_list=[None]*max_keys
        self.threshold_load_factor=threshold_load_factor
        self.keys_cnt=0
        self.resize_factor=resize_factor
        self.debug=debug

    def _get_load_factor(self):
        return self.keys_cnt/self.max_keys

    def _is_resize_needed(self):
        return self._get_load_factor()>=self.threshold_load_factor
    
    @abstractmethod
    def insert(self,key,value):
        raise NotImplementedError
    
    @abstractmethod
    def _resize(self):
        raise NotImplementedError
    
    @abstractmethod
    def delete(self,key):
        raise NotImplementedError
    
    @abstractmethod
    def get(self,key):
        raise NotImplementedError
    
    @abstractmethod
    def get_meta_data(self):
        raise NotImplementedError