import tensorflow as tf
import argparse
import os
import time


def print_t(string):
    print(f"{time.time_ns()}, {string}")


# get parameters from environment variables
folder_path = os.environ.get("FOLDER_PATH")
model_path = os.environ.get("MODEL_PATH")
model_name = os.environ.get("OUTPUT_PATH")

model_path = folder_path + model_path
model_name = folder_path + model_name

print_t(f"Converting model {model_path} to tflite")

# converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
# load the model
model = tf.keras.models.load_model(model_path)
# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open(model_name + ".tflite", "wb") as f:
    f.write(tflite_model)

print_t(f"Model {model_name} converted to tflite")
