# How to Run

Run `setup.sh` for environment buildup.
```
bash scripts/setup.sh
```

To run the simulation, run `main.py` in the root directory as
```
python main.py
```
under the configuration in `config/config.yaml`.

In this project, we implement 8 online paging algorithms of:
- OPT: Know about the next accessed time of each page, whenever we are required to evict a page, choose the page with the latest next accessed time.
- FIFO(first in, first out): Evict the page that was inserted earliest.
- LIFO(last in first out): Evict the page that was inserted last.
- LRU(least recently used): Allocate a timestamp to each page. A timestamp indicates the last time a page was used. Evict the page with the earliest timestamp.
- LFU(least frequently used): Evict the least frequently used page.
- Marking algorithm: A probabilistic algorithm with a $O(\log k)$-competitive ratio under the worst-case.
- SVM: The PrioISVM policy.
- LRUSVM: The space partitioning algorithm.