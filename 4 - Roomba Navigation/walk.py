from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper
import numpy as np
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, losses, Model, Input


class ConvLSTMAutoencoder(Model):
    def __init__(self, latent_dim, shape):
        super(ConvLSTMAutoencoder, self).__init__()
        self.latent_dim = latent_dim
        self.shape = shape
        self.encoder = tf.keras.Sequential([
            layers.ConvLSTM2D(8, (3, 3), activation="relu", padding="same", return_sequences=True, input_shape=shape),
            layers.MaxPooling3D((1, 2, 2), padding="same"),
            layers.ConvLSTM2D(16, (3, 3), activation="relu", padding="same", return_sequences=False),
            layers.Flatten(),
            layers.Dense(latent_dim, activation='relu'),
        ])
        self.decoder = tf.keras.Sequential([
            layers.Dense(np.prod((shape[0], shape[1]//2, shape[2]//2, 4)), activation='relu'),
            layers.Reshape((shape[0], shape[1]//2, shape[2]//2, 4)),
            layers.UpSampling3D((1, 2, 2)),
            layers.Conv3DTranspose(8, (3, 3, 3), activation='relu', padding="same"),
            layers.Conv3DTranspose(shape[3], (3, 3, 3), activation='sigmoid', padding="same")
        ])

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

shape = (1, 70, 210, 3)
latent_dim = 4
autoencoder = ConvLSTMAutoencoder(latent_dim, shape)
autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError(), metrics=["accuracy"])
# Print model summary
autoencoder.build(input_shape=(None, *shape))

# Fit the model
autoencoder.load_weights("autoencoder_4d_latent.keras")

input_layer = Input(shape=shape)
encoded_output = autoencoder.encoder(input_layer)
encoder_model = Model(inputs=input_layer, outputs=encoded_output)

unity_env = UnityEnvironment("./../linux/square_env/square.x86_64")
env = UnityToGymWrapper(unity_env, allow_multiple_obs=True)
# This resets the environment to an initial state and provides an initial observation
# - observations are three numpy arrays
obs_ego, obs_top, vectorial = env.reset()
# obs_ego is the observation that the robot-camera provides (your data)
# obs_top is a topdown view (debug only)
# vectorial contains non-visual signals:
# -> true/false if wall was hit (can be used)
# -> x-position, y-position, rotation angle (ground truth, debug only)

import matplotlib.pyplot as plt
fig = plt.figure(figsize = (10,10))
ax = plt.axes(projection='3d')

image_data = []

start = time.time()

"""n_degs = 180
for deg in range(n_degs):
    step_output = env.step([0,0, 2*np.pi/n_degs])
    obs_ego, obs_top, vectorial = step_output[0]
    image_data.append(obs_ego)"""
speed = 0.05
walks = [[0,speed],
         [speed,0],
         [0,-speed],
         [-speed,0],
         [0,speed],
         [speed,0]]
for walk in walks:
    print(f"Walking {walk}")
    while True:
        step_output = env.step([*walk, 0])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
        encoding = encoder_model.predict(obs_ego)
        ax.scatter(encoding[:,0],encoding[:,2],encoding[:,3], cmap="viridis")
        plt.show()
        if(vectorial[0] > 0):
            break

elapsed = time.time() - start
print(f"Took {elapsed:.2f}s")
np.save("path_0_images.npy", image_data)
print("Saved images")