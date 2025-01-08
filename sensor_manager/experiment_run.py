import time
import subprocess

spire_list = ["1", "5"]


# TODO:set up the managers


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

# clean topic metrics

# p = subprocess.Popen(["python3", "sensor_manager/clean_topic_metrics.py"])

# p.wait()


# python sensor_manager/experiment_run.py
