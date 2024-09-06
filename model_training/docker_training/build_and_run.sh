#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/training-regression:latest ./model_training/docker_training/
docker push lucaserf/training-regression:latest

# docker run lucaserf/python_tflite:latest /bin/bash
# kubectl rollout restart deployment/python-tflite-deploy

kubectl apply -f ./model_training/docker_training/app/deploy/training_deploy.yaml 
