#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/python_tflite:latest ./deploy_methods/python_code/docker_tflite_python
docker push lucaserf/python_tflite:latest

# docker run lucaserf/python_tflite:latest /bin/bash

kubectl apply -f ./deploy_methods/python_code/docker_tflite_python/app/deploy/python_tflite_deploy.yaml 

