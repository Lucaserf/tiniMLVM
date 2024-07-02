# mkdir Release
# cd Release
# cmake -DCMAKE_BUILD_TYPE=Release ..

# TYPE=$1
# BUILDDIR=build-$TYPE

# if [ ! -d $BUILDDIR ]; then
#     mkdir $BUILDDIR
# fi

# cd $BUILDDIR
cd ${HOME}/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release
make -j$(nproc-1)
#cmake -DCMAKE_BUILD_TYPE=Debug
cd ${HOME}/tiniMLVM/

./deploy_methods/c_code/tensorflow_lite_c/mnist/bin/tflite_inference > ${HOME}/tiniMLVM/mnist_test/tflite_c_inftime_mnist.csv
