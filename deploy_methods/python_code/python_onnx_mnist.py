import time
import numpy as np
import argparse
import onnxruntime as ort

parser = argparse.ArgumentParser()
parser.add_argument("--model_path", help="path to the model")
args = parser.parse_args()
model_path = args.model_path

print("timestamp[ns],inference_time[ns]")

# onnx model
providers = ["CPUExecutionProvider"]
session = ort.InferenceSession(model_path, providers=providers)

input_details = session.get_inputs()[0]
input_shape = input_details.shape
input_shape[0] = 1
input_shape = tuple(input_shape)
output_details = session.get_outputs()[0]

# read the input data
with open("./mnist_test/x_test.csv", "r") as f:
    data = f.readline()
    while data:
        # format the data as mnist image
        sample = np.array(data.split(","), dtype=np.float32).reshape(input_shape)
        t = time.time_ns()
        output = session.run(None, {input_details.name: sample})
        print("{},{}".format(time.time_ns(), time.time_ns() - t))
        data = f.readline()
