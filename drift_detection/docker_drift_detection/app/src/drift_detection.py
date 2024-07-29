import time
import numpy as np
import logging

import paho.mqtt.client as mqtt

from scipy.stats import ks_2samp

import pandas as pd

root = logging.getLogger()
root.setLevel(logging.INFO)

parameters = {
    "broker_address": "as-sensiblecity1.cloudmmwunibo.it",
    "topic_name": "test",
    "batch_size": 100,
    "alpha_p_value": 0.001,
}

data_folder = "/var/data/"


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
    # We only want to process n messages
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


def data_preprocessing(data):
    data = [x.decode("utf-8").split(",") for x in data]
    data = np.array(data, dtype=np.float32)
    # We are assuming that the first 10 values are the input and the last one is the label
    x = data[:, :-1]
    y = data[:, -1]
    return x, y


# get original training data
df_ref = pd.read_csv("./app/reference.csv").drop(columns=["y"]).values


# get input data from MQTT
while True:
    mqttc.user_data_set([])
    mqttc.connect(parameters["broker_address"])
    # sometimes if doesn't disconnect in time and gets more messages
    mqttc.loop_forever()
    t = time.time_ns()
    datax, datay = data_preprocessing(mqttc.user_data_get())
    # calculate Kolmogorov-Smirnov distance
    ks = ks_2samp(df_ref, datax)
    drift = [ks_p < parameters["alpha_p_value"] for ks_p in ks.pvalue]
    at_least_one_drift = any(drift)
    print(f"{t},{ks.pvalue},{at_least_one_drift}")

    # save data to file for retraining

    data_to_save = np.concatenate((datax, datay[:, np.newaxis]), axis=1)
    # save data with 5 decimal points
    if at_least_one_drift:
        with open(f"{data_folder}drift_data.csv", "a") as f:
            f.write(
                "\n".join([",".join([f"{x:.5f}" for x in row]) for row in data_to_save])
                + "\n"
            )
