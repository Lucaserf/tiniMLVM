import time
import subprocess

# get spire list from folder sensor_data
import os

spire_list = []
sensor_data_folder = f"sensor_manager/sensor_data/"
for file in os.listdir(sensor_data_folder):
    if file.startswith("spire_"):
        spire_list.append(file.split("_")[1])

# set up the managers # python sensor_manager/sensor_manager.py --sensor_id 1

# move the output to a file

print(f"spire_list: {spire_list}")

for spire in spire_list:
    subprocess.Popen(
        [
            "python3",
            "sensor_manager/sensor_manager.py",
            "--sensor_id",
            spire,
        ],
    )

# wait for managers to create neighbors
time.sleep(25)
# create data generators

for spire in spire_list:
    subprocess.Popen(
        ["python3", "sensor_manager/data_generator.py", "--sensor_id", spire]
    )

# from input to stop the data generation

time.sleep(2)

input("Press Enter to stop the data generation \n")

# stop data generators

for spire in spire_list:
    subprocess.Popen(
        ["pkill", "-f", f"python3 sensor_manager/data_generator.py --sensor_id {spire}"]
    )

# stop the managers

for spire in spire_list:
    subprocess.Popen(
        ["pkill", "-f", f"python3 sensor_manager/sensor_manager.py --sensor_id {spire}"]
    )

# clean topic metrics

# p = subprocess.Popen(["python3", "sensor_manager/clean_topic_metrics.py"])

# p.wait()


# python sensor_manager/experiment_run.py
