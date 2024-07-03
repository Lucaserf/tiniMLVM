#!bin/bash

model_path=$1
type=$2

echo "Running the Rust WebAssembly inference for the MNIST dataset with model $model_path and type $type"

cd ${HOME}/tiniMLVM/deploy_methods/wasm_code/mnist/rust

cargo build --target wasm32-wasi --release

cd ..

cp rust/target/wasm32-wasi/release/synthetic-data-regressor.wasm .

wasmedge compile synthetic-data-regressor.wasm out.wasm

cd ${HOME}/tiniMLVM/

wasmedge --dir .:. ./deploy_methods/wasm_code/mnist/out.wasm $model_path ./mnist_test/x_test.csv > ./mnist_test/tflite_wasm_inftime_mnist_$type.csv

# wasmedge --dir .:. synthetic-data-regressor.wasm model.tflite data_point.csv 




