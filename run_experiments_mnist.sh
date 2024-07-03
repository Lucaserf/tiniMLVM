#!/bin/bash

# Description: This script runs the experiments for the MNIST dataset.
model_type=$1

model_path="tflite_models/model_mnist_$model_type.tflite"

#python
python deploy_methods/python_code/python_tflite_mnist.py --model_path $model_path > mnist_test/tflite_python_inftime_mnist_$model_type.csv &

# sudo perf record -p $(pgrep -f deploy_methods/python_code/python_tflite_mnist.py) -g -- sleep 30

# #wasm
# bash deploy_methods/wasm_code/mnist/br_wasm_mnist.sh $model_path $model_type
# #c++
# bash deploy_methods/c_code/tensorflow_lite_c/mnist/run_tensorflow_lite.sh $model_path $model_type