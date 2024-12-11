# this manager reads data from an assigned sensor, detects drift, cooperates with neighbouring sensors to undestand if the drift is local or systematic, discriminating anomalies from drifts
# it stores data localy and shares it when needed for model training or calculating correlation between neighbouring sensors


import time
import numpy as np
import logging
import os
import re

import paho.mqtt.client as mqtt

from scipy.stats import ks_2samp

import pandas as pd

root = logging.getLogger()
root.setLevel(logging.INFO)

# get parameters from environment variables
# broker_address = os.getenv("BROKER_ADDRESS")
# topic_name = os.getenv("TOPIC_NAME")
# batch_size = int(os.getenv("BATCH_SIZE"))
# alpha_p_value = float(os.getenv("ALPHA_P_VALUE"))
# data_folder = os.getenv("FOLDER_PATH")
# output_name = os.getenv("OUTPUT_NAME")
sensor_id = 1
broker_sensor_address = "lserf-tinyml.cloudmmwunibo.it"
topic_name = f"sensor_{sensor_id}"
batch_size = 100
data_folder = f"sensor_manager/{topic_name}/"
alpha_p_value = 0.05

# create folder if it doesn't exist

if not os.path.exists(data_folder):
    os.makedirs(data_folder)


# reference data with higher version number
list_dir = os.listdir(data_folder)


# get the highest version number "reference_1.csv" -> 1

if len(list_dir) == 0:
    reference_df_name = "reference_0.csv"
else:
    reference_df_version = max([int(re.findall(r"\d+", x)[0]) for x in list_dir])
    reference_df_name = f"reference_{reference_df_version}.csv"

logging.info(f"Using reference data: {reference_df_name}")


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
    if len(userdata) >= batch_size:
        client.unsubscribe(topic_name)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logging.debug(
            f"Failed to connect: {reason_code}. loop_forever() will retry connection"
        )
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(topic_name, qos=1)


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# get input data from MQTT
while True:
    mqttc.user_data_set([])
    # logging.info("Connecting to {}".format(broker_address))
    mqttc.connect(broker_sensor_address)
    # sometimes if doesn't disconnect in time and gets more messages
    mqttc.loop_forever()
    t = time.time_ns()
    data = mqttc.user_data_get()

    data_values = np.array([int(i.decode()) for i in data])

    if os.path.exists(f"{data_folder}{reference_df_name}"):
        # load reference data
        with open(f"{data_folder}{reference_df_name}", "r") as f:
            df_ref = f.readlines()

        df_ref = [int(x[:-1]) for x in df_ref]
        # calculate Kolmogorov-Smirnov distance
        ks = ks_2samp(df_ref, data)
        drift = ks.pvalue < alpha_p_value

        # store data
        if drift:
            print("Drift detected")
        else:
            print("No drift detected")
            # rename old reference file
        with open(f"{data_folder}{reference_df_name}", "a") as f:
            f.write("\n".join([x.decode() for x in data]) + "\n")
    else:
        drift = False
        # store data
        with open(f"{data_folder}{reference_df_name}", "w") as f:
            f.write("\n".join([x.decode() for x in data]) + "\n")
