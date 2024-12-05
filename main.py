import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage.morphology import remove_small_objects, remove_small_holes
from scipy.spatial import ConvexHull
from loadcameradata import loadcameradata
from getsilhouette import getsilhouette
from findmodel import findmodel
from makevoxels import makevoxels
from carve import carve
from showsurface import showsurface
from colorsurface import colorsurface
from showscene import showscene
from project import project
from scipy.io import loadmat

cameras = loadcameradata('/images/')
for camera in cameras:
    camera["Silhouette"] = getsilhouette(camera["Image"])



# Step 2: Visualize Silhouettes
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(cameras[0]["Image"])
axs[0].set_title("Original Image")
axs[0].axis("off")
axs[1].imshow(cameras[0]["Silhouette"], cmap="gray")
axs[1].set_title("Silhouette")
axs[1].axis("off")
plt.tight_layout()
plt.show()

# Step 3: Determine Scene Limits
xlim, ylim, zlim = findmodel(cameras)

# Step 4: Create Voxel Array
voxels = makevoxels(xlim, ylim, zlim, 9000000)
voxels1 = makevoxels(xlim, ylim, zlim, 9000000)

voxels = carve(voxels, cameras[0])

print("Performing voxel carving with 36 views...")
starting_volume = len(voxels['XData'])
# for camera in cameras:
#     voxels = carve(voxels, camera)
print("Displaying initial carving result...")
for idx in range(36):  # Add more views
    voxels1 = carve(voxels1, cameras[idx])
showscene([cameras[idx]], voxels1)

final_volume = len(voxels['XData'])
print(f"Final volume is {final_volume} ({100 * final_volume / starting_volume:.2f}%)")
