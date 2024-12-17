# this manager reads data from an assigned sensor, detects drift, cooperates with neighbouring sensors to undestand if the drift is local or systematic, discriminating anomalies from drifts
# it stores data localy and shares it when needed for model training or calculating correlation between neighbouring sensors
import time
import numpy as np
import logging
import os
import re
import requests
import argparse

import paho.mqtt.client as mqtt

from scipy.stats import ks_2samp

root = logging.getLogger()
root.setLevel(logging.INFO)


argparser = argparse.ArgumentParser()
argparser.add_argument("--sensor_id", type=int, help="sensor id", required=True)

args = argparser.parse_args()

# get topic name from sensor id
sensor_id = args.sensor_id

list_dir = os.listdir("sensor_manager/sensor_data/")
for file in list_dir:
    if file.startswith(f"spire_{sensor_id}"):
        topic_name = f"{file}"[:-4]
        break

if topic_name is None:
    logging.error("Sensor not found")
    exit(1)


topic_name_data = topic_name.split("_")

position = topic_name_data[2]

radius = 10  # km radius
lat, lon = float(position.split(",")[0][1:]), float(position.split(",")[1][:-1])

topic_drift = f"drift/{position}"
topic_name = f"spire/{sensor_id}_{position}"

broker_sensor_address = "lserf-tinyml.cloudmmwunibo.it"

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


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print(
            "While unlikely (because on_publish() will be called after a network round-trip),"
        )
        print(" this is a race-condition that COULD happen")
        print("")
        print(
            "The best solution to avoid race-condition is using the msg_info from publish()"
        )
        print(
            "We could also try using a list of acknowledged mid rather than removing from pending list,"
        )
        print("but remember that mid could be re-used !")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.on_publish = on_publish

# get mqtt topics from emqx
APIkey = "46e50da2274c5b47"
secret_key = "5pLGNhmLxD9AISali37sxNZR0hbjEqKs8jjIbuoKDTZP"

# create topic

url = f"http://{broker_sensor_address}:18083/api/v5/mqtt/topic_metrics"
data = {"topic": topic_drift}
req = requests.post(
    url,
    json=data,
    auth=(APIkey, secret_key),
    headers={"Content-Type": "application/json"},
)


def get_topic_list(broker_sensor_address, APIkey, secret_key):
    url = f"http://{broker_sensor_address}:18083/api/v5/mqtt/topic_metrics"
    topics = []
    req = requests.get(
        url, auth=(APIkey, secret_key), headers={"Content-Type": "application/json"}
    )
    data = req.json()
    for topic in data:
        if topic["topic"].startswith("drift"):
            topics.append(topic["topic"])
    return topics


def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance


# get input data from MQTT
while True:
    mqttc.user_data_set([])
    unacked_publish = set()
    # logging.info("Connecting to {}".format(broker_address))
    mqttc.connect(broker_sensor_address)
    # sometimes if doesn't disconnect in time and gets more messages
    mqttc.loop_forever()
    t = time.time_ns()
    data = mqttc.user_data_get()

    data_values = np.array([int(i.decode()) for i in data])

    if os.path.exists(f"{data_folder}{reference_df_name}"):
        # load reference data
        # with open(f"{data_folder}{reference_df_name}", "r") as f:
        #     df_ref = f.readlines()

        # df_ref = [int(x[:-1]) for x in df_ref]
        df_ref = np.loadtxt(f"{data_folder}{reference_df_name}", dtype=int)

        # calculate Kolmogorov-Smirnov distance
        ks = ks_2samp(df_ref, data_values)
        drift = ks.pvalue < alpha_p_value

        # store data
        if drift:
            print("Drift detected")
            # signal that drift has been detected to the neighbours with timestamp
            drift_message = f"{time.time_ns()}"

            # msg_info = mqttc.publish(topic_drift, drift_message, qos=1)

            print("checking neighbours for drift")

            topic_list = get_topic_list(broker_sensor_address, APIkey, secret_key)

            for topic in topic_list:
                if topic != topic_drift:
                    position_n = topic.split("/")[-1]
                    lat_n, lon_n = position_n.split(",")
                    lat_n = float(lat_n[1:])
                    lon_n = float(lon_n[:-1])

                    distance = get_distance(lat, lon, lat_n, lon_n)

                    print("check distance between sensors")
                    print("Sensor 1: ", lat, lon)
                    print("Sensor 2: ", lat_n, lon_n)
                    print("Distance between sensors: ", distance)

                    if distance < radius:
                        print(f"Neighbour {topic} is in range")
                        # mqttc.publish(topic, drift_message, qos=1)
                    else:
                        print(f"Neighbour {topic} is out of range")

        else:
            print("No drift detected")
            # rename old reference file
        with open(f"{data_folder}{reference_df_name}", "a") as f:
            f.write("\n".join([str(x) for x in data_values]) + "\n")
    else:
        drift = False
        # store data
        with open(f"{data_folder}{reference_df_name}", "w") as f:
            f.write("\n".join([str(x) for x in data_values]) + "\n")
