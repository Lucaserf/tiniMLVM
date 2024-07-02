import tensorflow as tf
import time
import numpy as np

print("timestamp[ns],inference_time[ns]")

# tf lite model
interpreter = tf.lite.Interpreter(model_path="./tflite_models/model_mnist.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]

# read the input data
with open("./mnist_test/x_test.csv", "r") as f:
    data = f.readline()
    while data:
        # format the data as mnist image
        sample = np.array(data.split(","), dtype=np.float32).reshape(1, 28, 28, 1)
        t = time.time_ns()
        interpreter.set_tensor(input_details["index"], sample)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details["index"])
        print("{},{}".format(time.time_ns(), time.time_ns() - t))

        data = f.readline()
