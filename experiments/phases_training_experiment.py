import time
import subprocess
import argparse

# set print with timestamp

# run with:
# python experiments/drift_training_experiment.py --data_path ./experiments/<folder_name>

# get folder path
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, default="./experiments/data_phases1/")

data_path = parser.parse_args().data_path

# make the folder if it does not exist
subprocess.Popen(["mkdir", "-p", data_path])


def print_t(string):
    with open(f"{data_path}/experiment_logs.csv", "a") as f:
        f.write(f"{time.time_ns()}, {string}\n")


# start training the model without limitations

subprocess.Popen(
    [
        "kubectl",
        "apply",
        "-f",
        "./model_training/docker_training/app/deploy/training_deploy.yaml",
    ]
)

# wait for completion

# get job status

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

# save logs to a file
with open(f"{data_path}/alone_training_unlimited.log", "w") as f:
    f.write(logs.stdout.decode("utf-8"))


# delete the job
subprocess.Popen(["kubectl", "delete", "job", "training-job-test"])


# second phase testing


# unlimited training

subprocess.Popen(
    [
        "kubectl",
        "apply",
        "-f",
        "./model_training/docker_training/app/deploy/training_deploy.yaml",
    ]
)

time.sleep(5)

# limited training

subprocess.Popen(
    [
        "kubectl",
        "apply",
        "-f",
        "./model_training/docker_training/app/deploy/training_deploy_limited.yaml",
    ]
)

# wait for completion

# get job status

while True:
    jobs_test = subprocess.run(
        [
            "kubectl",
            "get",
            "jobs/training-job-test",
        ],
        stdout=subprocess.PIPE,
    )

    jobs_test_limited = subprocess.run(
        [
            "kubectl",
            "get",
            "jobs/training-job-test-limited",
        ],
        stdout=subprocess.PIPE,
    )

    if "Complete" in str(jobs_test.stdout) and "Complete" in str(
        jobs_test_limited.stdout
    ):
        break

# get logs

logs = subprocess.run(
    [
        "kubectl",
        "logs",
        "job/training-job-test",
    ],
    stdout=subprocess.PIPE,
)

# save logs to a file

with open(f"{data_path}/togheder_training_unlimited.log", "w") as f:
    f.write(logs.stdout.decode("utf-8"))

logs = subprocess.run(
    [
        "kubectl",
        "logs",
        "job/training-job-test-limited",
    ],
    stdout=subprocess.PIPE,
)

# save logs to a file

with open(f"{data_path}/togheder_training_limited.log", "w") as f:
    f.write(logs.stdout.decode("utf-8"))

# delete the jobs

subprocess.Popen(["kubectl", "delete", "job", "training-job-test"])

subprocess.Popen(["kubectl", "delete", "job", "training-job-test-limited"])


print(done)
