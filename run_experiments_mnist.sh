#!/bin/bash

# Description: This script runs the experiments for the MNIST dataset.
model_type=$1 #small, large, dense

model_path="tflite_models/model_mnist_$model_type.tflite"
onnx_model_path="onnx_models/model_mnist_$model_type.onnx"

#python
# python3 deploy_methods/python_code/python_tflite_mnist.py --model_path $model_path > mnist_test/tflite_python_inftime_mnist_$model_type.csv

#onnx
python3 deploy_methods/python_code/python_onnx_mnist.py --model_path $onnx_model_path > mnist_test/onnx_python_inftime_mnist_$model_type.csv

# get performance data from python

# cd perf/python_deploy
# while true
# do
#     ID=$(pgrep -f "./deploy_methods/python_code/python_tflite_mnist.py")
#     if [ -n "$ID" ]; then
#         break
#     fi
# done
# sudo perf record -p $ID -g -- sleep 30 
# cd ${HOME}/tiniMLVM/

#wasm
# bash deploy_methods/wasm_code/mnist/br_wasm_mnist.sh $model_path $model_type
#get performance data from wasm

# cd perf/wasm_deploy
# #loop until the wasm process starts and get the process id
# while true
# do
#     ID=$(pgrep -f "./deploy_methods/wasm_code/mnist/out.wasm")
#     if [ -n "$ID" ]; then
#         break
#     fi
# done
# sudo perf record -p $ID -g -- sleep 30

# cd ${HOME}/tiniMLVM/


#c++
# bash deploy_methods/c_code/tensorflow_lite_c/mnist/run_tensorflow_lite.sh $model_path $model_type

