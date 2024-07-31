FROM python:3.10
COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . ./

ENV PYTHONUNBUFFERED=1

#download training script
# RUN wget https://github.com/Lucaserf/tiniMLVM.git -O tflite_models/

#get name of script

#run training script
CMD ["python3","-u", "app/src/training.py"]