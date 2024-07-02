
#python
python deploy_methods/python_code/python_tflite_mnist.py > mnist_test/tflite_python_inftime_mnist.csv
#wasm
bash deploy_methods/wasm_code/mnist/br_wasm_mnist.sh
#c++
bash deploy_methods/c_code/tensorflow_lite_c/mnist/run_tensorflow_lite.sh 