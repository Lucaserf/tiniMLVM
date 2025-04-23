import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import os


#rsu position
rsu = [44.4901162203284, 11.3398356513878]

radius = 1000 #5 km

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the distance between two points on the Earth
    R = 6371e3  # Radius of the Earth in meters
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)

    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

folder_path_spires = "./sensor_data/"
spires_list = []

#load all spires in the radius
for file in os.listdir(folder_path_spires):
    if file.endswith(".csv"):
        #get the coordinates from the filename
        coordinates = file.split("_")[2].split("[")[1].split("]")[0].split(",")
        lat = float(coordinates[0])
        lon = float(coordinates[1])
        #calculate the distance
        distance = calculate_distance(rsu[0], rsu[1], lat, lon)
        print(f"Distance from RSU to {file}: {distance} m")
        if distance <= radius:
            spires_list.append(file)


#load all the dataframes



# #train the model
# X_data = []
# y_data = []

# seed = 42
# #set seed tensorflow backend

# tf.keras.utils.set_random_seed(seed)
# np.random.seed(seed)


# previous_values = 24

# for i in range(previous_values, len(df)):
#     X_data.append(df.iloc[i - previous_values:i, 0].values)
#     y_data.append(df.iloc[i, 0])

# X_data, y_data = np.array(X_data), np.array(y_data)

# #normalize the data
# scaler = MinMaxScaler(feature_range=(0, 1))

# X_data = scaler.fit_transform(X_data)
# y_data = scaler.fit_transform(y_data.reshape(-1, 1))


# #take the last week for testing
# X_test = X_data[-24*7:]
# y_test = y_data[-24*7:]

# #division of the dataset for training and validation
# X_train = X_data[:-24*7]
# y_train = y_data[:-24*7]
# #shuffle the training data

# X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
# X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


# #define callbacks for early stopping with validation loss

# #keep best model

# callbacks = [
#     tf.keras.callbacks.EarlyStopping(
#         monitor='val_loss',
#         patience=3,
#         verbose=1,
#     )
#     ,tf.keras.callbacks.ModelCheckpoint(
#         filepath='best_model.keras',
#         monitor='val_loss',
#         save_best_only=True,
#         verbose=1,
#     )
# ]


# model = tf.keras.models.Sequential([
#     tf.keras.layers.LSTM(32, input_shape=(previous_values,1), return_sequences=True),
#     tf.keras.layers.LSTM(32),
#     tf.keras.layers.Dense(1)
# ])

# model.compile(optimizer='adam', loss='mean_squared_error')



# model.fit(X_train, y_train, epochs=100, batch_size=32, callbacks=callbacks, shuffle=True, validation_split=0.2)