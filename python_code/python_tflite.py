import tensorflow as tf
import time
import numpy as np

print("timestamp[ns],inference_time[ns]")

# tf lite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]

# read the input data
with open("data.csv", "r") as f:
    data = f.readline()
    data = f.readline()
    while data:
        data = data.split(",")
        sample = np.array([[float(x) for x in data[:-1]]], dtype=np.float32)
        t = time.time_ns()
        interpreter.set_tensor(input_details["index"], sample)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details["index"])
        print("{},{}".format(time.time_ns(), time.time_ns() - t))

        data = f.readline()
