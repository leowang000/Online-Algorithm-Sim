import os
import sys
from .utils import Result, Scheduler
from tqdm import tqdm

class FIFO(Scheduler):
    def __init__(self, args):
        super().__init__(args)
        self.cache = []

    def run(self, requests):
        """
        Perform the FIFO algorithm on the given requests
        """
        self.result = Result(requests)

        for request in tqdm(requests, total = len(requests)):
            obj = request.obj_id
            if obj not in self.cache:
                self.result.cache_misses += 1
                if len(self.cache) == self.cache_size:
                    self.cache.pop(0)
                self.cache.append(obj)
        
        return self.result