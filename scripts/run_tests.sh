#!/bin/bash

# 定义算法和缓存大小的数组
algorithms=("SVM" "OPT")
cache_sizes=(4 8 16 32 64 512)

# 遍历所有算法
for alg in "${algorithms[@]}"; do
    # 遍历所有缓存大小
    for sz in "${cache_sizes[@]}"; do
        echo "运行: python3 main.py --algorithm $alg --cache_size $sz"
        python3 main.py --algorithm "$alg" --cache_size "$sz"
    done
done

echo "所有测试已完成!"