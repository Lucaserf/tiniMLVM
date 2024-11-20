import time
import subprocess
import argparse
import re

# set print with timestamp

# run with:
# python experiments/drift_training_experiment.py --data_path ./experiments/<folder_name>

# get folder path
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="./experiments/data_MLcreation/")

data_path = parser.parse_args().data_path

# make the folder if it does not exist
subprocess.Popen(["mkdir", "-p", data_path])

number_of_runs = 30

for _ in range(number_of_runs):
    # time to set up the persistent volume
    start_time = time.time_ns()

    # kubectl apply -f ./persistent_volume/data_volume.yaml
    # kubectl apply -f ./persistent_volume/data_volume_claim.yaml

    subprocess.Popen(
        [
            "kubectl",
            "apply",
            "-f",
            "./persistent_volume/data_volume.yaml",
        ]
    )
    time.sleep(1)

    subprocess.Popen(
        [
            "kubectl",
            "apply",
            "-f",
            "./persistent_volume/data_volume_claim.yaml",
        ]
    )

    while True:
        pv = subprocess.run(
            [
                "kubectl",
                "get",
                "pv",
            ],
            stdout=subprocess.PIPE,
        )

        if "Bound" in str(pv.stdout):
            break

    time_persistent_volume = time.time_ns() - start_time

    # transport (Emqx broker is already running), the topic is created by the subscriber

    # start training the model without limitations get time of start
    start_time_training = time.time_ns()

    subprocess.Popen(
        [
            "kubectl",
            "apply",
            "-f",
            "./model_training/docker_training/app/deploy/training_deploy.yaml",
        ]
    )

    while True:
        jobs = subprocess.run(
            [
                "kubectl",
                "get",
                "jobs",
            ],
            stdout=subprocess.PIPE,
        )

        if "Complete" in str(jobs.stdout):
            break

    # #get logs

    logs = subprocess.run(
        [
            "kubectl",
            "logs",
            "job/training-job-test",
        ],
        stdout=subprocess.PIPE,
    )

    logs = logs.stdout.decode("utf-8")

    # save logs to a file
    training_actually_started = int(
        re.findall(r"^(.*), Training started", logs, flags=re.MULTILINE)[0]
    )

    # delete the job
    subprocess.Popen(["kubectl", "delete", "job", "training-job-test"])

    time_start_training = training_actually_started - start_time_training
    # run drift detection

    time_drift_detection = time.time_ns()

    subprocess.Popen(
        [
            "kubectl",
            "apply",
            "-f",
            "./drift_detection/docker_drift_detection/app/deploy/drift_deploy.yaml",
        ]
    )

    # wait for drift detection to finish

    while True:
        jobs = subprocess.run(
            [
                "kubectl",
                "get",
                "deployments/drift-deploy",
            ],
            stdout=subprocess.PIPE,
        )

        if "1/1" in str(jobs.stdout):
            break

    time_drift_detection = time.time_ns() - time_drift_detection

    # get time to start inference, so conversion + the inference is ready

    time_start_inference = time.time_ns()

    subprocess.Popen(
        [
            "kubectl",
            "apply",
            "-f",
            "./deploy_methods/python_code/docker_tflite_python/app/deploy/python_tflite_deploy.yaml",
        ]
    )

    while True:
        jobs = subprocess.run(
            [
                "kubectl",
                "get",
                "deployments/python-tflite-deploy",
            ],
            stdout=subprocess.PIPE,
        )

        if "1/1" in str(jobs.stdout):
            break

    time_start_inference = time.time_ns() - time_start_inference

    # destroy drift detection

    subprocess.Popen(
        [
            "kubectl",
            "delete",
            "-f",
            "./drift_detection/docker_drift_detection/app/deploy/drift_deploy.yaml",
        ]
    )

    # destroy inference

    subprocess.Popen(
        [
            "kubectl",
            "delete",
            "-f",
            "./deploy_methods/python_code/docker_tflite_python/app/deploy/python_tflite_deploy.yaml",
        ]
    )

    # save times to a file

    with open(f"{data_path}/times.csv", "a") as f:
        f.write(
            f"{time_persistent_volume},{time_start_training},{time_drift_detection},{time_start_inference}\n"
        )

    # delete persistent volume

    subprocess.Popen(
        [
            "kubectl",
            "delete",
            "-f",
            "./persistent_volume/data_volume_claim.yaml",
        ]
    )

    time.sleep(1)

    subprocess.Popen(
        [
            "kubectl",
            "delete",
            "-f",
            "./persistent_volume/data_volume.yaml",
        ]
    )

    time.sleep(60)
