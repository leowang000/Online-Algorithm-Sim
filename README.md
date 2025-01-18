# Practical Paging Algorithms

## Introduction

This is the experimental part of CS1962-01 Online Algorithm of SJTU.

In this part, I tried several practical paging algorithms of:

- OPT
- FIFO
- LRU
- LFU
- LIFO
- Marking Algorithm

The experimental results are shown in the Lecture Notes ++.

## Get Started

For a quick start, you can use the compile.sh as
```
./compile.sh
```
to run compilation.

To run the simulation, you can use the `main.py` in the root directory as
```
python3 main.py
```
under the default configuration in `config/config.yaml`.

You can modify the configuration file to run different algorithms. We support command arguments, either. The format is as
```
python3 main.py --algorithm ALG --cache_size SIZE
```
There's a simple example:
```
python3 main.py --algorithm OPT --cache_size 64
```