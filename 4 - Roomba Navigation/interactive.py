import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
all_encode = np.load("all_encodings.npy")
zoom = all_encode[:500]
gradient = np.linspace(0, 1, zoom.shape[0])
fig = plt.figure(figsize = (10,10))

indices = (0,2,3)
ax = plt.axes(projection='3d')
#ax.scatter(zoom[:,indices[0]],zoom[:,indices[1]],zoom[:,indices[2]], c="blue", s=5)
image_encodings = np.load("degree_encodings_L.npy")
gradient = np.linspace(0, 1, image_encodings.shape[0])
ax.scatter(image_encodings[:,indices[0]],image_encodings[:,indices[1]],image_encodings[:,indices[2]], c="green",s=20)
image_encodings = np.load("room_scan_L_encodings.npy")
gradient = np.linspace(0, 1, image_encodings.shape[0])
ax.scatter(image_encodings[:,indices[0]],image_encodings[:,indices[1]],image_encodings[:,indices[2]], c=gradient, cmap="copper",s=20)
image_encodings = np.load("room_scan_L_90deg_encodings.npy")
gradient = np.linspace(0, 1, image_encodings.shape[0])
ax.scatter(image_encodings[:,indices[0]],image_encodings[:,indices[1]],image_encodings[:,indices[2]], c=gradient, cmap="cool",s=20)
#ii = [32,63,94,125] #path_0
ii = [14,32,250,270] # room_scan
"""for i in ii:
    ax.scatter(image_encodings[i,indices[0]],image_encodings[i,indices[1]],image_encodings[i,indices[2]], c="red",s=40)"""
plt.show()