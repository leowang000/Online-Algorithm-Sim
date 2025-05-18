import os
import sys
import argparse
import src.data_downloader as data_downloader
from src.input_processor import InputProcessor
from src.utils import MyNamespace
from src.scheduler import OPT, FIFO, LIFO, LRU, LFU, Marking, SVM, LRUSVM

def read_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            import yaml
            return MyNamespace(**yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type = str, default = "./config/config.yaml")
    parser.add_argument("--algorithm", type = str, default = "default")
    parser.add_argument("--cache_size", type = int, default = -1)
    parse_args = parser.parse_args()
    args = read_config(parse_args.config_file)

    if parse_args.algorithm != "default":
        args.algorithm = parse_args.algorithm
    if parse_args.cache_size != -1:
        args.cache_size = parse_args.cache_size

    print ("Practical Paging Algorithm Simulator")
    print (args)

    traces_list = data_downloader.download_data(args)
    
    print ("\n------------------------------------")

    input_processor = InputProcessor()
    output_file = os.path.join(args.output_dir, args.algorithm + f"_{args.cache_size}" + ".txt")

    if not os.path.exists(output_file):
        open(output_file, 'w').close()
    else:
        os.remove(output_file)
        open(output_file, 'w').close()

    for trace_file in traces_list:
        print (f"Processing {trace_file}")
        requests = input_processor.process_input(trace_file)

        scheduler = eval(args.algorithm)(args.cache_size)
        result = scheduler.run(requests)

        with open(output_file, 'a') as f:
            print (f"Total number of requests: {result.total_requests}")
            print (f"Total number of unique pages: {result.unique_pages}")
            print (f"Total number of cache misses: {result.cache_misses}")
            f.write(f"{trace_file}\t{result.total_requests}\t{result.unique_pages}\t{result.cache_misses}\n")

if __name__ == "__main__":
    main()