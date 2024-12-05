# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from skimage.morphology import remove_small_objects, remove_small_holes
# from scipy.spatial import ConvexHull
# from loadcameradata import loadcameradata
# from getsilhouette import getsilhouette
# from findmodel import findmodel
# from makevoxels import makevoxels
# from carve import carve
# from showsurface import showsurface
# from colorsurface import colorsurface
# from showscene import showscene
# from project import project
# # Import other necessary functions (loadcameradata, getsilhouette, carve, etc.)

# # Step 1: Load Camera and Image Data
# #data = loadmat('datafile.mat')
# cameras = loadcameradata('/Users/varunsatheesh/BVCProjects/SpaceCarving/SpaceCarving/images/')
# camera_positions = np.array([camera['rawP'] for camera in cameras])
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(camera_positions[:, 0], camera_positions[:, 1], camera_positions[:, 2])
# ax.set_title("Camera Positions")
# plt.show()

# # Step 2: Visualize Silhouettes
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# print(type(cameras[0]["Silhouette"]))
# axs[0].imshow(cameras[0]["Image"])
# axs[0].set_title("Original Image")
# axs[0].axis("off")
# axs[1].imshow(cameras[0]["Silhouette"], cmap="gray")
# axs[1].set_title("Silhouette")
# axs[1].axis("off")
# plt.tight_layout()
# plt.show()

# # Step 3: Determine Scene Limits
# xlim, ylim, zlim = findmodel(cameras)

# # Step 4: Create Voxel Array
# voxels = makevoxels(xlim, ylim, zlim, 6000000)
# voxels1 = makevoxels(xlim, ylim, zlim, 6000000)

# # Step 5: Carve with the First Camera
# voxels = carve(voxels, cameras[0])

# # # Visualize
# # showscene(cameras[:1], voxels)

# # # Step 6: Refine with Additional Views
# # for idx in [3, 6]:  # Add more views
# #     voxels = carve(voxels, cameras[idx])

# # showscene(cameras[:3], voxels)

# # Step 7: Final Carving with All Cameras
# print("Performing voxel carving with 36 views...")
# starting_volume = len(voxels['XData'])
# # for camera in cameras:
# #     voxels = carve(voxels, camera)
# print("Displaying initial carving result...")
# for idx in range(0,35,5):  # Add more views
#     voxels1 = carve(voxels1, cameras[idx])
# showscene(cameras[:35], voxels1)

# # Display the result after initial carvings

# #ptch = showsurface(voxels)


# final_volume = len(voxels['XData'])
# print(f"Final volume is {final_volume} ({100 * final_volume / starting_volume:.2f}%)")

# # # Refinement process to assign scores
# # print("Refining voxel values...")
# # offset_vec = (1 / 3) * voxels['Resolution'] * np.array([-1, 0, 1])
# # off_x, off_y, off_z = np.meshgrid(offset_vec, offset_vec, offset_vec)

# # num_voxels = len(voxels['Value'])
# # num_offsets = off_x.size
# # scores = np.zeros(num_voxels)

# # for jj in range(num_offsets):
# #     keep = np.ones(num_voxels, dtype=bool)
# #     myvoxels = voxels.copy()
# #     myvoxels['XData'] = voxels['XData'] + off_x.flat[jj]
# #     myvoxels['YData'] = voxels['YData'] + off_y.flat[jj]
# #     myvoxels['ZData'] = voxels['ZData'] + off_z.flat[jj]

# #     for camera in cameras:
# #         mykeep = carve(myvoxels, camera)
# #         keep[np.setdiff1d(np.arange(num_voxels), mykeep, assume_unique=True)] = False

# #     scores[keep] += 1

# # # Normalize scores and update voxel values
# # voxels['Value'] = scores / num_offsets

# # # Display the refined result
# # # print("Displaying refined voxel result...")
# # # ptch = showsurface(voxels)
# # showscene(cameras, voxels)


# # # Final result with coloring
# # print("Applying colors to the voxel model...")
# # ptch = showsurface(voxels)
# # colorsurface(ptch, cameras)
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
# Import other necessary functions (loadcameradata, getsilhouette, carve, etc.)

# Step 1: Load Camera and Image Data
#data = loadmat('datafile.mat')
#mat_data = loadmat('/Users/varunsatheesh/BVCProjects/SpaceCarving/SpaceCarving/images/datafile.mat')
cameras = loadcameradata('/Users/varunsatheesh/BVCProjects/SpaceCarving/SpaceCarving/images/')
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

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(voxels['XData'], voxels['YData'], voxels['ZData'], s=1)
# plt.title("Initial Voxel Grid")
# plt.show()

# Step 5: Carve with the First Camera
voxels = carve(voxels, cameras[0])

# # Visualize
# showscene(cameras[:1], voxels)

# # Step 6: Refine with Additional Views
# for idx in [3, 6]:  # Add more views
#     voxels = carve(voxels, cameras[idx])

# showscene(cameras[:3], voxels)

# Step 7: Final Carving with All Cameras
print("Performing voxel carving with 36 views...")
starting_volume = len(voxels['XData'])
# for camera in cameras:
#     voxels = carve(voxels, camera)
print("Displaying initial carving result...")
for idx in range(36):  # Add more views
    voxels1 = carve(voxels1, cameras[idx])
showscene([cameras[idx]], voxels1)
# for idx in range(0,5):  # Add more views
#     voxels1 = carve(voxels1, cameras[idx])
# for idx in range(12,15):  # Add more views
#     voxels1 = carve(voxels1, cameras[idx])

# showscene(cameras[12:35], voxels1)

# Display the result after initial carvings

#ptch = showsurface(voxels)


final_volume = len(voxels['XData'])
print(f"Final volume is {final_volume} ({100 * final_volume / starting_volume:.2f}%)")

# # Refinement process to assign scores
# print("Refining voxel values...")
# offset_vec = (1 / 3) * voxels['Resolution'] * np.array([-1, 0, 1])
# off_x, off_y, off_z = np.meshgrid(offset_vec, offset_vec, offset_vec)

# num_voxels = len(voxels['Value'])
# num_offsets = off_x.size
# scores = np.zeros(num_voxels)

# for jj in range(num_offsets):
#     keep = np.ones(num_voxels, dtype=bool)
#     myvoxels = voxels.copy()
#     myvoxels['XData'] = voxels['XData'] + off_x.flat[jj]
#     myvoxels['YData'] = voxels['YData'] + off_y.flat[jj]
#     myvoxels['ZData'] = voxels['ZData'] + off_z.flat[jj]

#     for camera in cameras:
#         mykeep = carve(myvoxels, camera)
#         keep[np.setdiff1d(np.arange(num_voxels), mykeep, assume_unique=True)] = False

#     scores[keep] += 1

# # Normalize scores and update voxel values
# voxels['Value'] = scores / num_offsets

# # Display the refined result
# # print("Displaying refined voxel result...")
# # ptch = showsurface(voxels)
# showscene(cameras, voxels)


# # Final result with coloring
# print("Applying colors to the voxel model...")
# ptch = showsurface(voxels)
# colorsurface(ptch, cameras)