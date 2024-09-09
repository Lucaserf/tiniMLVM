import tensorflow as tf
import time
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model_path", help="path to the model")
args = parser.parse_args()


print("timestamp[ns],inference_time[ns]")

# tf lite interpreter without delegate
interpreter = tf.lite.Interpreter(
    model_path=args.model_path,
    num_threads=1,
)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]
input_shape = input_details["shape"]
# read the input data
with open("./mnist_test/x_test.csv", "r") as f:
    data = f.readline()
    while data:
        # format the data as mnist image

        sample = np.array(data.split(","), dtype=np.float32).reshape(input_shape)
        t = time.time_ns()
        interpreter.set_tensor(input_details["index"], sample)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details["index"])
        run_time = time.time_ns() - t
        print("{},{}".format(time.time_ns(), run_time))
        data = f.readline()
