import yaml
import time
import subprocess


# run drift detection pod

subprocess.run(
    [
        "kubectl",
        "apply",
        "-f",
        "./drift_detection/docker_drift_detection/app/deploy/drift_deploy.yaml",
    ]
)
time.sleep(5)
