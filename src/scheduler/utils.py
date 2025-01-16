class Result:
    def __init__(self, requests):
        self.total_requests = len(requests)
        self.unique_pages = len(set([request.obj_id for request in requests]))
        self.cache_misses = 0
        
class Scheduler:
    def __init__(self, args):
        self.cache_size = args.cache_size
    
    def run(self):
        raise NotImplementedError