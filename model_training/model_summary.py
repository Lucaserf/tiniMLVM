import tensorflow as tf


# load model

model = tf.keras.models.load_model("tf_models/mnist_model_dense.h5")

model.summary()
