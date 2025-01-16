import os
import sys
import heapq
from .utils import Result, Scheduler
from tqdm import tqdm

class OPTObject:
    def __init__(self, obj_id, next_access_vtime):
        self.obj_id = obj_id
        self.next_access_vtime = next_access_vtime
    
    def __lt__(self, other):
        return self.next_access_vtime > other.next_access_vtime

    def __str__(self):
        return f"Object {self.obj_id} with next access time {self.next_access_vtime}"
    
    def __repr__(self):
        return f"Object {self.obj_id} with next access time {self.next_access_vtime}"

class OPT(Scheduler):
    def __init__(self, args):
        super().__init__(args)
        self.cache = []

    def run(self, requests):
        """
        Perform the OPT algorithm on the given requests
        """
        self.result = Result(requests)

        for request in tqdm(requests, total = len(requests)):
            obj_id = request.obj_id
            next_access = request.next_access_vtime
            if next_access == -1:
                next_access = 1e12
            if not any(page.obj_id == obj_id for page in self.cache):
                self.result.cache_misses += 1
                if len(self.cache) == self.cache_size:
                    heapq.heappop(self.cache)
                heapq.heappush(self.cache, OPTObject(obj_id, next_access))
        
        return self.result