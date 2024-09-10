#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/converting-lite:latest ./model_training/docker_lite_converter/
docker push lucaserf/converting-lite:latest

# docker run lucaserf/python_tflite:latest /bin/bash
# kubectl rollout restart deployment/python-tflite-deploy

# kubectl apply -f ./model_training/docker_training/app/deploy/training_deploy.yaml 
