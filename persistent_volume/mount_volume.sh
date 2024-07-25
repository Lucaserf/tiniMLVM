#!bin/bash

cd ${HOME}/tiniMLVM/
# This script is used to mount a volume in a kubernetes cluster

kubectl apply -f ./persistent_volume/data_volume.yaml
kubectl apply -f ./persistent_volume/data_volume_claim.yaml
