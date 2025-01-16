import os
import sys
import argparse
import data_downloader

def read_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            import yaml
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", type = str, default = "../config/config.yaml")
    args = parser.parse_args()
    args = read_config(args.config_file)

    traces_list = data_downloader.download_data(args)

    for trace in traces_list:
        print (trace)

if __name__ == "__main__":
    main()