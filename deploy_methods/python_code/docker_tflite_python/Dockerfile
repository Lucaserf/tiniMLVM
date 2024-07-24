FROM python:3.10
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . ./

ENV PYTHONUNBUFFERED=1

#download model
# RUN wget https://github.com/Lucaserf/tiniMLVM.git -O tflite_models/

CMD ["python3","-u", "app/src/python_tflite_mnist.py"]