import sys
import struct
from .utils import Request

class InputProcessor:
    def process_input(self, trace_file):
        requests = self._parse_trace(trace_file)
        return requests

    def _parse_trace(self, trace_file):
        # format string for unpacking binary data
        # '<' means little-endian
        # 'I': uint32_t, 4 bytes
        # 'Q': uint64_t, 8 bytes
        # 'q': int64_t, 8 bytes
        format_str = '<IQIq'
    
        record_size = struct.calcsize(format_str)
    
        requests = []
    
        with open(trace_file, 'rb') as f:
            while True:
                chunk = f.read(record_size)
                if len(chunk) != record_size:
                    if len(chunk) == 0:
                        break
                    print (f"Invalid chunk size: {len(chunk)} in trace {trace_file}", file = sys.stderr)
                    exit(1)
            
                unpacked_data = struct.unpack(format_str, chunk)
            
                request = Request(*unpacked_data)
                requests.append(request)
    
        return requests