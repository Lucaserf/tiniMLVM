#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/drift_detection:latest ./drift_detection/docker_drift_detection
docker push lucaserf/drift_detection:latest

# docker run lucaserf/python_tflite:latest /bin/bash


#kubectl rollout restart deployment/drift-deploy

kubectl apply -f ./drift_detection/docker_drift_detection/app/deploy/drift_deploy.yaml 
# kubectl delete -f ./drift_detection/docker_drift_detection/app/deploy/drift_deploy.yaml 

