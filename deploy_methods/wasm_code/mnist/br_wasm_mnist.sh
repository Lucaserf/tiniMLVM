#!bin/bash

cd ${HOME}/tiniMLVM/deploy_methods/wasm_code/mnist/rust

cargo build --target wasm32-wasi --release

cd ..

cp rust/target/wasm32-wasi/release/synthetic-data-regressor.wasm .

wasmedge compile synthetic-data-regressor.wasm out.wasm

cd ${HOME}/tiniMLVM/

wasmedge --dir .:. ./deploy_methods/wasm_code/mnist/out.wasm ./tflite_models/model_mnist.tflite ./mnist_test/x_test.csv > ./mnist_test/tflite_wasm_inftime_mnist.csv

# wasmedge --dir .:. synthetic-data-regressor.wasm model.tflite data_point.csv 




