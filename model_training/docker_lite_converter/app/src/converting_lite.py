import tensorflow as tf
import argparse
import os

# get model path from arguments
parser = argparse.ArgumentParser()
parser.add_argument("--folder_path", help="folder kubernetes", default="/var/data/")
parser.add_argument(
    "--model_path", help="path to the model", default="regression_model_tf"
)
parser.add_argument(
    "--model_name", help="name of the model", default="regression_model_tf"
)
args = parser.parse_args()

model_path = args.folder_path + args.model_path
model_name = args.folder_path + args.model_name


converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
tflite_model = converter.convert()


with open(model_name + ".tflite", "wb") as f:
    f.write(tflite_model)
