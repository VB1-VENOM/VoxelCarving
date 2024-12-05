import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from showcamera import showcamera
from showsurface import showsurface

def showscene(cameras, voxels=None):
    """
    SHOWSCENE: Display a carve scene, including cameras, images, and the model.

    Parameters:
    cameras (list): List of camera dictionaries, each containing data such as position and orientation.
    voxels (dict, optional): Voxel data containing 'XData', 'YData', 'ZData' for the model surface.

    Example:
    >>> cameras = loadcameradata("data", [1])
    >>> cameras[0]["Silhouette"] = getsilhouette(cameras[0]["Image"])
    >>> voxels = carve(makevoxels([-1, 1], [-1, 1], [-1, 1], 50), cameras[0])
    >>> showscene(cameras, voxels)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set data aspect ratio
    ax.set_box_aspect([1, 1, 1])

    # Plot each camera center
    #print("cameras",cameras)
    for camera in cameras:
        showcamera(ax, camera)

    # Label axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show a surface around the object if voxel data is provided
    
    if voxels is not None and len(voxels['XData']) > 0:
        #print("voxels as showscene",voxels)
        showsurface(voxels,ax)

    # Adjust view and lighting
    ax.view_init(elev=20, azim=30)
    ax.grid(True)
    ax.set_title("Scene with Cameras and Voxels")

    plt.tight_layout()
    plt.show()