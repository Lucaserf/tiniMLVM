import tensorflow as tf
import argparse
import os

# get parameters from environment variables
folder_path = os.environ.get("FOLDER_PATH")
model_path = os.environ.get("MODEL_PATH")
model_name = os.environ.get("OUTPUT_PATH")

model_path = folder_path + model_path
model_name = folder_path + model_name


converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
tflite_model = converter.convert()


with open(model_name + ".tflite", "wb") as f:
    f.write(tflite_model)
