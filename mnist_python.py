#mnist test 
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf



with open('./data/t10k-images-idx3-ubyte', 'rb') as f:
    x_test = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)

with open('./data/t10k-labels-idx1-ubyte', 'rb') as f:
    y_test = np.frombuffer(f.read(), np.uint8, offset=8)


with open('./data/train-images-idx3-ubyte', 'rb') as f:
    x_train = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)

with open('./data/train-labels-idx1-ubyte', 'rb') as f:
    y_train = np.frombuffer(f.read(), np.uint8, offset=8)


model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(28 * 28,)),
    tf.keras.layers.Dense(64, activation='sigmoid'),
    tf.keras.layers.Dense(64, activation='sigmoid'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test, y_test, verbose=2)


image = x_test[0]
plt.imshow(image.reshape(28,28), cmap='gray')
plt.savefig('mnist.png')

print(model.predict(x_test[:1]))

image = x_test[1]
plt.imshow(image.reshape(28,28), cmap='gray')
plt.savefig('mnist_1.png')

print(model.predict(x_test[1:2]))
