#!/bin/bash

# Pour glouton et approx
for n in {"1000","2500","5000","7500","10000"}; do
    ./inst_gen.py -s $n -n 5 -x test_set/GA/GA
done

# Pour tous les algorithmes
for n in {"5","10","15","20","25"}; do
    ./inst_gen.py -s $n -n 5 -x test_set/DP/DP
done
