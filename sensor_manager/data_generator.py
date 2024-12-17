import time
import paho.mqtt.client as mqtt
import numpy as np
import os


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


sensor_id = 1
broker_sensor_address = "lserf-tinyml.cloudmmwunibo.it"
sensor_data_folder = f"sensor_manager/sensor_data/"

# find csv name with sensor id
for file in os.listdir(sensor_data_folder):
    if file.startswith(f"spire_{sensor_id}"):
        sensor_data_folder = f"{sensor_data_folder}{file}"
        break


topic_name = f"spire/{sensor_id}_{file.split('_')[-1]}"

number_messages = 500
frequency = 100

print("generating data for sensor: ", sensor_id)
print("sending data to topic: ", topic_name)
print("number of messages: ", number_messages)
print("frequency: ", frequency)


def main():
    # get args from command line

    unacked_publish = set()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)
    mqttc.connect(
        broker_sensor_address
    )  # 192.168.17.48:18083 server address  mqtt.eclipseprojects.io, as-sensiblecity1.cloudmmwunibo.it
    # set client identifier
    mqttc.loop_start()

    n_messages = 0

    # Our application produce some messages

    if int(number_messages) == -1:
        while True:
            with open(sensor_data_folder, "r") as f:
                line = f.readline()[:-1]
                while line != "":
                    msg_info = mqttc.publish(topic_name, line, qos=1)
                    n_messages += 1
                    unacked_publish.add(msg_info.mid)
                    time.sleep(1 / frequency)
                    line = f.readline()[:-1]
    else:
        with open(sensor_data_folder, "r") as f:
            line = f.readline()[:-1]
            while line != "" and n_messages < int(number_messages):
                msg_info = mqttc.publish(topic_name, line, qos=1)
                n_messages += 1
                unacked_publish.add(msg_info.mid)
                time.sleep(1 / frequency)
                line = f.readline()[:-1]

    # for i in range(10):
    #     msg_info2 = mqttc.publish("prova_topic", "message2", qos=1)
    #     unacked_publish.add(msg_info2.mid)

    # Wait for all message to be published
    while len(unacked_publish):
        time.sleep(0.1)

    # Due to race-condition described above, the following way to wait for all publish is safer
    msg_info.wait_for_publish()
    # msg_info2.wait_for_publish()

    mqttc.disconnect()
    mqttc.loop_stop()


if __name__ == "__main__":
    main()
