import requests


broker_sensor_address = "lserf-tinyml.cloudmmwunibo.it"


# get mqtt topics from emqx
APIkey = "ab5cb9200eff8dc1"
secret_key = "7o7oToPD8tHAYGWtbWVOUPWPEAv9Adk11PyWaC9ByzHZK"


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


def delete_topic_metrics(broker_sensor_address, APIkey, secret_key, topic):
    # url = (
    #     f"http://{broker_sensor_address}:18083/api/v5/mqtt/topic_metrics/"
    #     + "{"
    #     + str(topic)
    #     + "}"
    # )
    topic = topic.replace(" ", "%20")
    topic = topic.replace(",", "%2C")
    topic = topic.replace("[", "%5B")
    topic = topic.replace("]", "%5D")
    topic = topic.replace("/", "%2F")

    url = f"http://{broker_sensor_address}:18083/api/v5/mqtt/topic_metrics/{topic}"

    req = requests.delete(
        url,
        auth=(APIkey, secret_key),
        headers={"Content-Type": "application/json"},
    )
    return req


topic_list = get_topic_list(broker_sensor_address, APIkey, secret_key)


for topic in topic_list:
    response = delete_topic_metrics(broker_sensor_address, APIkey, secret_key, topic)
    if response.status_code == 204:
        print(f"Deleted topic {topic}")
    else:
        print(f"Error deleting topic {topic}")
        print(response.text)

# check if the topics are deleted

topic_list = get_topic_list(broker_sensor_address, APIkey, secret_key)

print(f"Remaining topics: {topic_list}")


# clean spire reference data and outputs

import os

sensor_data_folder = "sensor_manager/manager_data/"
spire_folder = "sensor_manager/spire/"

for file in os.listdir(sensor_data_folder):
    os.remove(sensor_data_folder + file)

for file in os.listdir(spire_folder):
    # convert file to literal string
    file = repr(file)

    # remove folder and his files
    os.system(f"rm -r {spire_folder + file}")


# python sensor_manager/clean_topic_metrics.py
