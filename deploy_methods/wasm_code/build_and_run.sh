#!bin/bash

cd rust

cargo build --target wasm32-wasi --release

cd ..

cp rust/target/wasm32-wasi/release/synthetic-data-regressor.wasm .

wasmedge compile synthetic-data-regressor.wasm out.wasm

wasmedge --dir .:. out.wasm model.tflite data.csv > wasm_times.csv

# wasmedge --dir .:. synthetic-data-regressor.wasm model.tflite data_point.csv 




