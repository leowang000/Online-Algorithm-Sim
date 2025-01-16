from types import SimpleNamespace
from typing import NamedTuple, List

class Request(NamedTuple):
    timestamp: int
    obj_id: int
    obj_size: int
    next_access_vtime: int

class MyNamespace(SimpleNamespace):
    def __str__(self):
        print ("------------------------------------")
        print ("Configuration:")
        dict = self.__dict__
        for key, value in dict.items():
            print(f"\t{key} : {value}")
        print ("------------------------------------")
        return ""