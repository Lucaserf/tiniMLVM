#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/c_tflite:latest ./deploy_methods/c_code/tensorflow_lite_c/docker_lite_c
docker push lucaserf/c_tflite:latest

# docker run lucaserf/python_tflite:latest /bin/bash
# kubectl rollout restart deployment/python-tflite-deploy

# kubectl apply -f ./deploy_methods/python_code/docker_tflite_python/app/deploy/python_tflite_deploy.yaml 

