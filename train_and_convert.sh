model_type=$1

python model_training/tfmodel_training_mnist.py --type_model $model_type

python model_training/lite_converter.py --model_path tf_models/mnist_model_tf_$model_type --model_name model_mnist_$model_type