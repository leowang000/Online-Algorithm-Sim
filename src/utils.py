from types import SimpleNamespace
from typing import NamedTuple, List
from .cpp_utils import _parse_trace

class MyNamespace(SimpleNamespace):
    def __str__(self):
        print ("------------------------------------")
        print ("Configuration:")
        dict = self.__dict__
        for key, value in dict.items():
            print(f"\t{key} : {value}")
        print ("------------------------------------")
        return ""