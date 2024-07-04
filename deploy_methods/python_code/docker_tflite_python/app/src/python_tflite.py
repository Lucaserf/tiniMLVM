import tensorflow as tf
import time
import numpy as np
import os
import logging

import paho.mqtt.client as mqtt


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        logging.debug(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        logging.debug(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        logging.debug(
            "unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)"
        )
    else:
        logging.debug(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    userdata.append(message.payload)

    # We only want to process 10 messages
    if len(userdata) >= parameters["batch_size"]:
        client.unsubscribe(parameters["topic_name"])


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logging.debug(
            f"Failed to connect: {reason_code}. loop_forever() will retry connection"
        )
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(parameters["topic_name"], qos=1)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe


print("timestamp[ns],inference_time[ns]")

# get environment variables
model_name = os.environ.get("MODEL_NAME")
model_path = "./tflite_models/model_name"


# tf lite model
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]

input_shape = input_details["shape"]

# get input data from MQTT
# read the input data
with open("./mnist_test/x_test.csv", "r") as f:
    data = f.readline()
    while data:
        # format the data as mnist image

        t = time.time_ns()
        sample = np.array(data.split(","), dtype=np.float32).reshape(input_shape)
        interpreter.set_tensor(input_details["index"], sample)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details["index"])
        print("{},{}".format(time.time_ns(), time.time_ns() - t))
        data = f.readline()
