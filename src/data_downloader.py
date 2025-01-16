import zstandard as zstd
import shutil
import subprocess
import sys
import os
import re
from tqdm import tqdm

def download_data_from_url(dataset_url, dataset_path):
    """
    Download data from a URL and save it to a specified path
    """
    try:
        result = subprocess.run([
            "wget",
            "-r",
            "-l1",
            "--no-parent",
            "-A",
            ".zst",
            "-nd",
            "-P",
            dataset_path,
            dataset_url,
        ], check = True) 
    except: 
        print("Error downloading the data")
        sys.exit(1)

def decompress_zst(dataset_path):
    """
    Decompress all .zst files in a directory
        @param dataset_path: path to the directory containing the .zst files
        @return: a list of the decompressed files
    """
    with os.scandir(dataset_path) as entries:
        data_list = []
        os.chdir(dataset_path)
        for entry in tqdm(entries, desc = "Decompressing .zst files"):
            if entry.is_file() and entry.name.endswith(".zst"):
                with open(entry, 'rb') as compressed_file:
                    # Do not decompress if the file is already decompressed
                    if entry.name.rstrip(".zst") not in os.listdir(dataset_path):
                        with open(entry.name.rstrip('.zst'), 'wb') as destination:
                            dctx = zstd.ZstdDecompressor()
                            with dctx.stream_reader(compressed_file) as reader:
                                shutil.copyfileobj(reader, destination)
                                data_list.append(os.path.join(dataset_path, entry.name.rstrip('.zst')))
                    else:
                        data_list.append(os.path.join(dataset_path, entry.name.rstrip('.zst')))
    
    return data_list

def download_data(args):
    """
    Download and decompress data from a URL, if it has not been downloaded yet
        @param args: a dictionary containing the dataset URL and the path to save the dataset
        @return data_list: a sorted list of the decompressed files
    """
    dataset_url = args.dataset_url
    dataset_path = args.dataset_path

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
        download_data_from_url(dataset_url, dataset_path)

    data_list = decompress_zst(dataset_path)

    # sort the data_list
    data_list = sorted(data_list, key = lambda x: -int(re.search(r'\d+', x).group()))

    data_list = data_list[:args.num_to_test]

    return data_list
