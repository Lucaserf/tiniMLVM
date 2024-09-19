import subprocess
import time
import argparse

# get folder path
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="./experiments/")
data_path = parser.parse_args().data_path

while True:
    try:
        # get logs from the drift detection pod
        pod_names = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                "default",
            ],
            stdout=subprocess.PIPE,
        )

        for line in pod_names.stdout.decode("utf-8").split("\n"):
            if "drift" in line:
                pod_name = line.split(" ")[0]
                break

        logs_pod = subprocess.run(
            [
                "kubectl",
                "logs",
                pod_name,
                "-n",
                "default",
            ],
            stdout=subprocess.PIPE,
        )

        # save logs to a file
        with open(f".{data_path}/{pod_name}.log", "w") as f:
            f.write(logs_pod.stdout.decode("utf-8"))

        time.sleep(5)
    except:
        time.sleep(5)
