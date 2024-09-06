FROM python:3.10
COPY requirements.txt .

#update pip
RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
COPY . ./

ENV PYTHONUNBUFFERED=1

#download training script
# RUN wget https://github.com/Lucaserf/tiniMLVM.git -O tflite_models/



#run training script
CMD ["python3","-u", "app/src/training.py", "--data_path", "reference.csv"]