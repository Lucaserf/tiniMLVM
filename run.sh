#!/bin/bash

gcc -march=native -O3 -o prova genann_times.c genann.c -lm
./prova
rm ./prova
