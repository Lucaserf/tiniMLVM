import tensorflow as tf
import argparse
import os

# get model path from arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_path",
    help="path to the model",
    default="./data_kind/regression_model_tf_prova.keras",
)
parser.add_argument("--model_name", help="name of the model", default="tflite_prova")
args = parser.parse_args()

model_path = args.model_path
model_name = args.model_name


# converter = tf.lite.TFLiteConverter.from_saved_model(model_path)

# load the model
model = tf.keras.models.load_model(model_path)

# Convert the model.

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()


with open("./" + model_name + ".tflite", "wb") as f:
    f.write(tflite_model)
