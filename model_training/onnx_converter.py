import tf2onnx
import tensorflow as tf
import argparse
import os
import onnx

# get model path from arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model_path", help="path to the model")
parser.add_argument("--model_name", help="name of the model")
args = parser.parse_args()

model_path = args.model_path
model_name = args.model_name

# model = tf.saved_model.load(model_path)
model = tf.keras.models.load_model(model_path)

config = model.get_config()
shape = model.layers[0].input.shape
input_dtype = model.layers[0].input.dtype
input_name = model.layers[0].input.name

# right now it works only for models with one input
spec = (tf.TensorSpec(shape=shape, dtype=input_dtype, name=input_name),)
saving_path = "./onnx_models/" + model_name + ".onnx"

# convert model to onnx
onnx_model, _ = tf2onnx.convert.from_keras(
    model, input_signature=spec, opset=13, output_path=saving_path
)
