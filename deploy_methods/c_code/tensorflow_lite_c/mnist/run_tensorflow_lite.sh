# mkdir Release
# cd Release
# cmake -DCMAKE_BUILD_TYPE=Release ..


model_path=$1
type=$2
echo "Running the C++ TensorFlow Lite inference for the MNIST dataset with model $model_path and type $type"

cd ${HOME}/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release
make -j$(nproc)
#cmake -DCMAKE_BUILD_TYPE=Debug
cd ${HOME}/tiniMLVM/

./deploy_methods/c_code/tensorflow_lite_c/mnist/bin/tflite_inference $model_path > ${HOME}/tiniMLVM/mnist_test/tflite_c_inftime_mnist_$type.csv
