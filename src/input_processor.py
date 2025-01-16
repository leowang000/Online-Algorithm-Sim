import sys
import struct
from .utils import _parse_trace

class InputProcessor:
    def process_input(self, trace_file):
        requests = _parse_trace(trace_file)
        return requests
