#! /bin/bash

cd ${HOME}/tiniMLVM/

docker build -t lucaserf/python_tflite:latest ./deploy_methods/python_code/docker_tflite_mnist
docker push lucaserf/logging_agent:latest

docker run lucaserf/python_tflite:latest /bin/bash

