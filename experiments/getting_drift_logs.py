import subprocess
import time
import argparse

# get folder path
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="./experiments/")
data_path = parser.parse_args().data_path

while True:
    try:
        # get pod names
        pod_names = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                "default",
                "--no-headers",
            ],
            stdout=subprocess.PIPE,
        )
        # get and write logs from every pod
        for line in pod_names.stdout.decode("utf-8").split("\n")[0:-1]:
            pod_name = line.split(" ")[0]
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
            with open(f"./{data_path}/{pod_name}.log", "w") as f:
                f.write(logs_pod.stdout.decode("utf-8"))

        time.sleep(5)
    except:
        time.sleep(5)
