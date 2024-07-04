FROM python:3.10
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . ./

ENV PYTHONUNBUFFERED=1

CMD ["python3","-u", "app/src/python_tflite_mnist.py"]