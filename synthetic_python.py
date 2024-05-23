import numpy as np
import tensorflow as tf
import time

epochs = 10  # Number of epochs


def synthetic_function():
    # return non linear formula with 10 features
    x = np.random.rand(10)
    a = [1, 4, 1, 1, 1, 1, 6, 1, 1, 1]
    e = [2, 2, 2, 6, 2, 3, 2, 3, 2, 2]
    return x, sum([a[i] * x[i] ** e[i] for i in range(10)])


# defining model class
class RegressionModel:
    def __init__(self):
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Input(shape=(10,)),
                tf.keras.layers.Dense(64, activation="sigmoid"),
                tf.keras.layers.Dense(64, activation="sigmoid"),
                tf.keras.layers.Dense(1, activation="linear"),
            ]
        )
        self.optimizer = tf.keras.optimizers.Adam()
        self.time_inference = 0
        self.time_train = 0

    def train_step(self, data, label):
        with tf.GradientTape() as tape:
            t_start = int(time.time())
            data = np.expand_dims(data, axis=0)
            prediction = self.model(data, training=True)
            self.time_inference = time.time() - t_start
            t = time.time()
            loss = tf.reduce_mean(tf.square(label - prediction))
            grads = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
            self.time_train = time.time() - t
            print("{},{},{}".format(t_start, self.time_train, self.time_inference))

    def predict(self, data):
        t = time.time()
        data = np.expand_dims(data, axis=0)
        output = self.model(data)
        print("Inference time: ", time.time() - t)
        return output


# print("initializing the model")

print("timestamp,train_time,train_inference_time")
print("{},{},{}".format(int(time.time()), 0.0, 0.0))

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

for epoch in range(epochs):
    sample, label = synthetic_function()
    model.train_step(sample, label)

model.predict(np.random.rand(10))
