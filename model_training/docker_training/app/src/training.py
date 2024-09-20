import numpy as np
import tensorflow as tf
import time
import argparse
import os

input_size = 10


def print_t(string):
    print(f"{time.time_ns()}, {string}")


# defining model class
class RegressionModel:
    def __init__(self):
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Input(shape=(input_size,)),
                tf.keras.layers.Dense(64, activation="sigmoid"),
                tf.keras.layers.Dense(64, activation="sigmoid"),
                tf.keras.layers.Dense(1, activation="linear"),
            ]
        )
        self.optimizer = tf.keras.optimizers.Adam()

    def train_step(self, data, label):
        with tf.GradientTape() as tape:
            t_start = time.time_ns()
            data = np.expand_dims(data, axis=0)
            prediction = self.model(data, training=True)
            loss = tf.reduce_mean(tf.square(label - prediction))
            grads = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    def predict(self, data):
        data = np.expand_dims(data, axis=0)
        output = self.model(data)
        return output


model = RegressionModel()

# training on batch
# print("training the model with synthetic data batches")
# for epoch in range(epochs):
#     print(f"Epoch {epoch+1}/{epochs}")
#     batch = np.random.rand(batch_size, 10)
#     model.train_on_batch(batch, np.array([synthetic_function(x) for x in batch]))
#     evaluate_batch = np.random.rand(evaluate_size, 10)
#     model.evaluate(evaluate_batch, np.array([synthetic_function(x) for x in evaluate_batch]), verbose=2)


# get arguments from environment variables
folder_path = os.environ.get("FOLDER_PATH")
data_path = os.environ.get("DATA_PATH")
output_path = os.environ.get("OUTPUT_PATH")
logging_level = os.environ.get("LOGGING_LEVEL")
rename = os.environ.get("RENAME")

print_t("Training started")

with open(folder_path + data_path, "r") as f:
    data = f.readline()
    data = f.readline()
    while data:
        t = time.time()
        data = data.split(",")
        sample = np.array([float(x) for x in data[:-1]])
        label = float(data[-1])
        model.train_step(sample, label)
        data = f.readline()

print_t("Training finished")
# save model
# tf.saved_model.save(model.model, folder_path + output_path)

# save .keras model
model.model.save(folder_path + output_path + ".keras")

# delete reference file


# rename the data file
# os.rename(folder_path + data_path, folder_path + rename)
