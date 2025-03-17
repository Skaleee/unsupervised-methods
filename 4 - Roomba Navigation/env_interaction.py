from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper
import numpy as np
import time

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

image_data = []

start = time.time()

n_degs = 360
speed = 1

"""step_output = env.step([200,0,0])
for deg in range(n_degs):
    step_output = env.step([0,0, 2*np.pi/n_degs])
    obs_ego, obs_top, vectorial = step_output[0]
    image_data.append(obs_ego)"""

"""walks = [[0,.5],
         [0.5,0],
         [0,-.5],
         [-.5,0],
         [0,.5],
         [0.5,0],]

for walk in walks:
    print("Turning")
    for deg in range(n_degs):
        step_output = env.step([0,0, 2*np.pi/n_degs])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
    print(f"Walking {walk}")
    while True:
        step_output = env.step([*walk, 0])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
        if(vectorial[0] > 0):
            print(len(image_data))
            break"""

step_output = env.step([0,0, 2*np.pi/4])
#walk to -1,-1 of environment
while True:
        step_output = env.step([-1,0, 0])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
        if(vectorial[0] > 0):
            break
while True:
        step_output = env.step([0,-1, 0])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
        if(vectorial[0] > 0):
            break

#walk in a snake manner through all positions of environment
current_dir = 1
while True:
    """print("Turning")
    for deg in range(n_degs):
        step_output = env.step([0,0, 2*np.pi/n_degs])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)"""
    step_output = env.step([current_dir*speed,0, 0])
    obs_ego, obs_top, vectorial = step_output[0]
    image_data.append(obs_ego)
    if(vectorial[0] > 0):
        print(f"Turning ({len(image_data)})")
        """for deg in range(n_degs):
            step_output = env.step([0,0, 2*np.pi/n_degs])
            obs_ego, obs_top, vectorial = step_output[0]
            image_data.append(obs_ego)"""
        current_dir *= -1
        step_output = env.step([0, speed, 0])
        obs_ego, obs_top, vectorial = step_output[0]
        image_data.append(obs_ego)
        if(vectorial[0] > 0):
             break

elapsed = time.time() - start
print(f"Took {elapsed:.2f}s")
np.save("room_scan_images_90deg.npy", image_data)
print(f"Saved {len(image_data)} images")
