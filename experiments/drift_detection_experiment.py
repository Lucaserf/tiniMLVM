import time
import subprocess

# set print with timestamp

# run with python experiments/drift_detection_experiment.py > ./experiments/drift_experiment.log


def print_t(string):
    print(f"{time.time_ns()}, {string}")


# copy reference data from the regression_test folder
subprocess.Popen(["cp", "./regression_test/reference.csv", "./data_kind/reference.csv"])


# run ctrldrift operator
subprocess.Popen(["kubectl", "apply", "-f", "./experiments/ctrldrift.yaml"])
print_t("Starting ctrldrift operator")


### sending reference data and after some time start sending data with drift

# start sending reference data
send_reference = subprocess.Popen(
    [
        "python3",
        "./publishers/mqttpub_reg.py",
        "--data_path",
        "./regression_test/reference.csv",
    ]
)
print_t("Sending reference data")

# start saving logs from drift detection pod
saving_logs = subprocess.Popen(["python", "./experiments/getting_drift_logs.py"])

# wait a command to change the data
input("")
# time.sleep(2 * 60)

# stop publishing reference data
send_reference.kill()
print_t("Stopping reference data")

# start sending data with drift
pub_drift = subprocess.Popen(
    [
        "python3",
        "publishers/mqttpub_reg.py",
        "--data_path",
        "./regression_test/data.csv",
        "--n_messages",
        "-1",
    ]
)
print_t("Sending drift data")

# wait a command to stop the drift with input from user
input("")

# stop publishing drift data
pub_drift.kill()
print_t("Stopping drift data")


###collect data from the drift detection operator logs and save it to a file

# get pod provider name
pods = subprocess.run(
    [
        "kubectl",
        "get",
        "pods",
        "-n",
        "crossplane-system",
    ],
    stdout=subprocess.PIPE,
)

# find provider-driftprovider in the string
for line in pods.stdout.decode("utf-8").split("\n"):
    if "provider-driftprovider" in line:
        pod_name = line.split(" ")[0]
        break

# get logs from the drift detection operator

logs = subprocess.run(
    [
        "kubectl",
        "logs",
        pod_name,
        "-n",
        "crossplane-system",
    ],
    stdout=subprocess.PIPE,
)


# save logs to a file
with open("./experiments/drift_detection_logs.log", "w") as f:
    f.write(logs.stdout.decode("utf-8"))


# # stop ctrldrift operator
subprocess.Popen(["kubectl", "delete", "-f", "./experiments/ctrldrift.yaml"])

print_t("Stopping ctrldrift operator")


# stop saving logs from drift detection pod
saving_logs.kill()
