# Online-Algorithm-Sim

## Introduction

This project is developed to perform evaluation of the online paging algorithms introduced in CS1962 of SJTU, taught by [Prof. Yuhao Zhang](http://www.zyhwtc.com/) and [Prof. Zhihao Tang](http://simecv.sufe.edu.cn/page.aspx?id=9).

We implement a efficient simulation system combined with a well-designed frontend. This simulation system runs the simulation of specific online paging algorithm on well-designed and widely-used dataset automatically by identifying the URL of the dataset in the configuration file.

## Get started

You need to clone the repo first:
```
https://github.com/WhiteCmile/Online-Algorithm-Sim
```

### Environment buildup

We provide some scripts for quick environment buildup
```
bash scripts/setup.sh
```

### Quick start with default configuration

To run the simulation, you can use the `main.py` in the root directory as
```
python3 main.py
```
under the default configuration in `config/config.yaml`.

### Customize your configuration

You can modify the configuration file to run different algorithms. We support command arguments, either. The format is as
```
python3 main.py --algorithm ALG --cache_size SIZE
```
There's a simple example:
```
python3 main.py --algorithm OPT --cache_size 64
```

Besides, you can choose the dataset for free by changing the `dataset_url` and `num_to_test` in the `config/config.yaml`.

For example, if you would like to perform an evaluation of Twitter, this can be easily implemented by resetting the `config/config.yaml`:
```
dataset_url: https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/twitter/
```
<font color="red">We do not recommand this since the traces are too large:(</font>

## Supported algorithms

In this project, we implement 6 online paging algorithms of:
- OPT: Know about the next accessed time of each page, whenever we are required to evict a page, choose the page with the latest next accessed time.
- FIFO(first in, first out): Evict the page that was inserted earliest.
- LIFO(last in first out): Evict the page that was inserted last.
- LRU(least recently used): Allocate a timestamp to each page. A timestamp indicates the last time a page was used. Evict the page with the earliest timestamp.
- LFU(least frequently used): Evict the least frequently used page.
- Marking algorithm: A probabilistic algorithm with a $O(\log k)$-competitive ratio under the worst-case.

## Acknowledgements

We sincerely thanks the [libCacheSim](https://github.com/1a1a11a/libCacheSim) for their open-source dataset.

The dataset can be found in [here](https://ftp.pdl.cmu.edu/pub/datasets/twemcacheWorkload/cacheDatasets/), where this simulation system can run all the traces of this dataset.