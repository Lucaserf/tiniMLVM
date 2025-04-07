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
    if file.startswith(f"spire_{sensor_id}_"):
        topic_name = f"{file}"[:-4]
        break

if topic_name is None:
    logging.error("Sensor not found")
    exit(1)


def print_log(log):
    with open(f"sensor_manager/manager_data/output_{sensor_id}.txt", "a") as f:
        f.write(log + "\n")


topic_name_data = topic_name.split("_")

position = topic_name_data[2]

radius = 150e-3  # km radius
lat, lon = float(position.split(",")[0][1:]), float(position.split(",")[1][:-1])

topic_drift = f"drift/{sensor_id}_{position}"
topic_name = f"spire/{sensor_id}_{position}"

broker_sensor_address = "lserf-tinyml.cloudmmwunibo.it"

batch_size = int(24 * 30 * 4)  # x months of data
data_folder = f"sensor_manager/{topic_name}/"
alpha_p_value = 1e-10
threshold_local = 0.4
drift_time = None
drift_checked = 0

# create folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)


# reference data with higher version number
list_dir = os.listdir(data_folder)


# get the highest version number "reference_1.csv" -> 1

if len(list_dir) == 0:
    reference_df_name = "reference_0.csv"
    reference_df_version = 0
else:
    reference_df_version = max([int(re.findall(r"\d+", x)[0]) for x in list_dir])
    reference_df_name = f"reference_{reference_df_version}.csv"

# print_log(f"Using reference data: {reference_df_name}")


# get mqtt topics from emqx
APIkey = "ab5cb9200eff8dc1"
secret_key = "7o7oToPD8tHAYGWtbWVOUPWPEAv9Adk11PyWaC9ByzHZK"

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
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    r = 6371  # Radius of the earth in km
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = r * c  # Distance in km
    return distance


def check_neighbours_drift(
    time_detection, neighbours_drifts, time_window, threshold=threshold_local
):
    # check if drift is local or systematic
    num_neighbours = len(neighbours_drifts)
    # if no neighbours the drift is systematic (we cannot detect locality)
    if num_neighbours == 0:
        return True, 1
    num_drifts = 0
    # check if drift is local
    for neighbour in neighbours_drifts:
        drifts = neighbours_drifts[neighbour]
        if len(drifts) == 0:
            pass
        else:
            for drift in drifts:
                if abs(time_detection - drift) < time_window:
                    num_drifts += 1
                    # print_log(
                    #     f"the distance between the local drift and neighbour is {(time_detection - drift)/1e9} seconds"
                    # )
                    break
    value = num_drifts / num_neighbours
    if value > threshold:
        return True, value
    else:
        return False, value


# wait for all the sensors managers to be up
time.sleep(10)
# print_log("Sensor manager is checking for neighbours")
topic_list = get_topic_list(broker_sensor_address, APIkey, secret_key)

topic_connect_list = []

for topic in topic_list:
    if topic != topic_drift:
        id_n = topic.split("_")[0].split("/")[-1]
        position_n = topic.split("_")[1].split("/")[-1]
        lat_n, lon_n = position_n.split(",")
        lat_n = float(lat_n[1:])
        lon_n = float(lon_n[:-1])

        distance = get_distance(lat, lon, lat_n, lon_n)

        # print_log("check distance between sensors")
        # print_log(f"Sensor 1 {lat} , {lon}")
        # print_log(f"Sensor {id_n} {lat_n} , {lon_n}")
        # print_log(f"Distance between sensors: {distance}")

        if distance < radius:
            # print_log(f"Neighbour {topic} is in range")
            topic_connect_list.append(topic)
        else:
            pass
            # print_log(f"Neighbour {topic} is out of range")

# print_log all the neighbours

print_log(f"Neighbours: {topic_connect_list}")


# creation of data structure for storing neighbours drifts
neighbours_drifts = {}

for topic in topic_connect_list:
    neighbours_drifts[topic] = []


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

    if message.topic == topic_name:
        userdata.append(message.payload)
        # We only want to process n messages
        # if len(userdata) >= batch_size:
        #     client.unsubscribe(topic_name)
    else:

        payload = message.payload.decode()

        # print_log(
        #     f"Drift detected from neighbour, {message.topic}, timestamp: {payload}"
        # )
        neighbours_drifts[message.topic].append(int(payload))


def on_connect(client, userdata, flags, reason_code, properties):
    global topic_connect_list

    if reason_code.is_failure:
        logging.debug(
            f"Failed to connect: {reason_code}. loop_forever() will retry connection"
        )
    else:
        # subscribe to sensor
        client.subscribe(topic_name, qos=1)

        # subscribe to close sensor managers
        for topic in topic_connect_list:
            client.subscribe(topic, qos=1)


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    # try:
    #     userdata.remove(mid)
    # except KeyError:
    #     print_log("on_publish() is called with a mid not present in unacked_publish")
    #     print_log("This is due to an unavoidable race-condition:")
    #     print_log("* publish() return the mid of the message sent.")
    #     print_log("* mid from publish() is added to unacked_publish by the main thread")
    #     print_log("* on_publish() is called by the loop_start thread")
    #     print_log(
    #         "While unlikely (because on_publish() will be called after a network round-trip),"
    #     )
    #     print_log(" this is a race-condition that COULD happen")
    #     print_log("")
    #     print_log(
    #         "The best solution to avoid race-condition is using the msg_info from publish()"
    #     )
    #     print_log(
    #         "We could also try using a list of acknowledged mid rather than removing from pending list,"
    #     )
    #     print_log("but remember that mid could be re-used !")
    pass


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.on_publish = on_publish

# get input data from MQTT
while True:
    mqttc.user_data_set([])
    unacked_publish = set()
    # print_log("Connecting to {}".format(broker_address))
    mqttc.connect(broker_sensor_address)
    # sometimes if doesn't disconnect in time and gets more messages
    # mqttc.loop_forever()
    mqttc.loop_start()

    # with 20 days at second frequency we have 24*20 messages in a second

    # the time window has to be between the period of messages on drift checks

    # batch_size / (frequency * 2) * 1e9

    time_window = 10 * 1e9

    while True:

        data = mqttc.user_data_get()

        if len(data) < batch_size:
            if drift_time is not None:
                drift_time = int(drift_time)
                if time.time_ns() - drift_time > time_window:
                    systematic_drift, value_neigh = check_neighbours_drift(
                        drift_time,
                        neighbours_drifts,
                        time_window=time_window,
                        threshold=threshold_local,
                    )

                    if systematic_drift:
                        print_log(
                            f"Systematic drift detected with reference file {reference_df_name}, period = {drift_checked}, p_value = {ks.pvalue}, ks_statistics = {ks.statistic} , threshold = {value_neigh}, direction = {direction}"
                        )
                        # create the next reference file
                        reference_df_version += 1
                        reference_df_name = f"reference_{reference_df_version}.csv"
                        with open(f"{data_folder}{reference_df_name}", "w") as f:
                            f.write("\n".join([str(x) for x in data_values]) + "\n")
                        with open(
                            f"{data_folder}systematicdrift_{reference_df_name}", "w"
                        ) as f:
                            f.write("\n".join([str(x) for x in data_values]) + "\n")

                        # if systematic drift is detected, we should start saving to a new reference file
                    else:
                        print_log(
                            f"Local drift detected with reference file {reference_df_name}, period = {drift_checked}, p_value = {ks.pvalue}, ks_statistics = {ks.statistic}, threshold = {value_neigh}, direction = {direction}"
                        )
                        with open(
                            f"{data_folder}localdrift_{reference_df_name}", "w"
                        ) as f:
                            f.write("\n".join([str(x) for x in data_values]) + "\n")
                    drift_time = None
            time.sleep(1e-3)
            continue

        data_values = np.array([float(i.decode()) for i in data])

        if os.path.exists(f"{data_folder}{reference_df_name}"):
            # load reference data
            # with open(f"{data_folder}{reference_df_name}", "r") as f:
            #     df_ref = f.readlines()

            # df_ref = [int(x[:-1]) for x in df_ref]
            df_ref = np.loadtxt(f"{data_folder}{reference_df_name}", dtype=float)

            # calculate Kolmogorov-Smirnov distance
            ks = ks_2samp(df_ref, data_values)
            drift = ks.pvalue < alpha_p_value

            drift_checked += 1

            # store data
            if drift:
                # print_log(f"Drift detected, p_value = {ks.pvalue}")
                # signal that drift has been detected to the neighbours with timestamp
                drift_time = f"{time.time_ns()}"
                msg_info = mqttc.publish(topic_drift, drift_time, qos=1)

                direction = np.mean(data_values) - np.mean(df_ref)

                direction = 1 if direction > 0 else 0

                # unacked_publish.add(msg_info.mid)
            else:
                print_log(
                    f"No drift detected, period = {drift_checked}, p_value = {ks.pvalue}, ks_statistics = {ks.statistic}"
                )
                reference_df_version += 1
                reference_df_name = f"reference_{reference_df_version}.csv"
                with open(f"{data_folder}{reference_df_name}", "w") as f:
                    f.write("\n".join([str(x) for x in data_values]) + "\n")

        else:
            drift = False
            # store data
            with open(f"{data_folder}{reference_df_name}", "w") as f:
                f.write("\n".join([str(x) for x in data_values]) + "\n")

        # clear data from buffer
        mqttc.user_data_set([])

# python sensor_manager/sensor_manager.py --sensor_id 1
