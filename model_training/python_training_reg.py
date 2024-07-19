import numpy as np
import tensorflow as tf
import time


input_size = 10


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
            time_inference = time.time_ns() - t_start
            t = time.time_ns()
            loss = tf.reduce_mean(tf.square(label - prediction))
            grads = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
            time_train = time.time_ns() - t
            print("{},{},{}".format(t_start, time_train, time_inference))

    def predict(self, data):
        t = time.time()
        data = np.expand_dims(data, axis=0)
        output = self.model(data)
        print("Inference time: ", time.time() - t)
        return output


# print("initializing the model")

print("timestamp[ns],train_time[ns],train_inference_time[ns]")
# print("{},{},{}".format(int(time.time()), 0.0, 0.0))

model = RegressionModel()

# training on batch
# print("training the model with synthetic data batches")
# for epoch in range(epochs):
#     print(f"Epoch {epoch+1}/{epochs}")
#     batch = np.random.rand(batch_size, 10)
#     model.train_on_batch(batch, np.array([synthetic_function(x) for x in batch]))
#     evaluate_batch = np.random.rand(evaluate_size, 10)
#     model.evaluate(evaluate_batch, np.array([synthetic_function(x) for x in evaluate_batch]), verbose=2)


# training on samples
# print("training the model with synthetic data samples")

with open("./regression_test/data.csv", "r") as f:
    data = f.readline()
    data = f.readline()
    while data:
        t = time.time()
        data = data.split(",")
        sample = np.array([float(x) for x in data[:-1]])
        label = float(data[-1])
        model.train_step(sample, label)
        data = f.readline()

# save model
tf.saved_model.save(model.model, "tf_models/regression_model_tf")

# save .keras model
model.model.save("tf_models/regression_model.keras")
