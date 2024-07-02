#!/bin/bash

gcc -march=native -O3 -o genann_times genann_times.c genann.c -lm
./genann_times > genann_times.csv
rm ./genann_times
