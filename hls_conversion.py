import time
import numpy as np
import argparse
import onnx
import hls4ml


# parser = argparse.ArgumentParser()
# parser.add_argument("--model_path", help="path to the model")
# args = parser.parse_args()
# model_path = args.model_path

model_path = "onnx_models/model_mnist_small.onnx"

# onnx model
onnx_model = onnx.load(model_path)

# Convert the ONNX model to a HLS model
hls_model = hls4ml.converters.convert_from_onnx_model(onnx_model)

# Print the HLS model configuration
hls4ml.utils.plot_model(hls_model, show_shapes=True, show_precision=True, to_file=None)

# Compile the HLS model
hls_model.compile()

# Write the HLS project to a directory
hls_model.write()
