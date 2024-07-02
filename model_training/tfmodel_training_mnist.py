import numpy as np
import tensorflow as tf
import os


# defining model class
class MnistModel:
    def __init__(self):
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Input(shape=(28, 28, 1)),
                tf.keras.layers.Conv2D(
                    32,
                    kernel_size=(3, 3),
                    activation="relu",
                ),
                tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dense(10, activation="softmax"),
            ]
        )
        self.optimizer = tf.keras.optimizers.Adam()

    def train_step(self, data, label):
        with tf.GradientTape() as tape:
            prediction = self.model(data, training=True)
            loss = tf.reduce_mean(
                tf.keras.losses.sparse_categorical_crossentropy(label, prediction)
            )
            grads = tape.gradient(loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    def predict(self, data):
        output = self.model(data)
        return output


# get data from mnist
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_val, y_val) = mnist.load_data()
x_train, x_val = x_train / 255.0, x_val / 255.0
x_train = np.expand_dims(x_train, axis=-1)
x_val = np.expand_dims(x_val, axis=-1)

# initialize the model
mnist_model = MnistModel()


chkpt = "mnist_model.h5"
# training the model with callback on validation data
es_cb = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=2, verbose=1, mode="auto"
)
cp_cb = tf.keras.callbacks.ModelCheckpoint(
    filepath=chkpt, monitor="val_loss", verbose=0, save_best_only=True, mode="auto"
)

mnist_model.model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
mnist_model.model.fit(
    x_train,
    y_train,
    epochs=100,
    validation_data=(x_val, y_val),
    callbacks=[es_cb, cp_cb],
)
# load the best model
mnist_model.model = tf.keras.models.load_model(chkpt)

# save the model
tf.saved_model.save(mnist_model.model, "mnist_model_tf")

# delete the .keras model
os.remove(chkpt)

# save test data as csv
np.savetxt("x_test.csv", x_val.reshape(-1, 28 * 28), delimiter=",")
