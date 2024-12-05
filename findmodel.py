import numpy as np
from makevoxels import makevoxels
from carve import carve
from getcameradirection import getcameradirection
def findmodel(cameras):
    """
    FINDMODEL: Locate the model to be carved relative to the cameras.

    Parameters:
    cameras (list): A list of camera dictionaries, each containing at least:
                    - 'T': The camera position (numpy array).
                    - 'Direction': The direction the camera is looking at.

    Returns:
    tuple: (xlim, ylim, zlim) representing the bounding box for the model.
    """
    # Concatenate camera positions
    camera_positions = np.column_stack([camera['T'] for camera in cameras])

    # Compute initial x, y, and z limits
    xlim = [np.min(camera_positions[0, :]), np.max(camera_positions[0, :])]
    ylim = [np.min(camera_positions[1, :]), np.max(camera_positions[1, :])]
    zlim = [np.min(camera_positions[2, :]), np.max(camera_positions[2, :])]

    # Compute zlim based on where each camera is looking
    range_factor = 0.6 * np.sqrt((np.diff(xlim) ** 2) + (np.diff(ylim) ** 2))
    for camera in cameras:
        viewpoint = camera['T'] - range_factor * getcameradirection(camera)
        zlim[0] = min(zlim[0], viewpoint[2])
        zlim[1] = max(zlim[1], viewpoint[2])
    expand_factor = 0.75
    # Adjust the x and y limits inward by a quarter of their ranges
    xrange = np.diff(xlim)[0]
    xlim = [xlim[0] - expand_factor * xrange, xlim[1] + expand_factor * xrange]
    yrange = np.diff(ylim)[0]
    ylim = [ylim[0] - expand_factor * yrange, ylim[1] + expand_factor * yrange]
    # zrange = np.diff(zlim)[0]
    # zlim = [zlim[0] - expand_factor * zrange, zlim[1] + expand_factor * zrange]
    
    # Create initial voxel volume and perform rough space-carving
    voxels = makevoxels(xlim, ylim, zlim, 6000000)
    for camera in cameras:
        voxels = carve(voxels, camera)
    #print("one done")

    # Ensure there is something left after carving
    if len(voxels['XData']) == 0:
        raise ValueError("Nothing left after initial search! Check your camera matrices.")

    # Expand limits based on the found voxel data and resolution
    resolution = voxels['Resolution']
    xlim = [min(voxels['XData']) - 2 * resolution, max(voxels['XData']) + 2 * resolution]
    ylim = [min(voxels['YData']) - 2 * resolution, max(voxels['YData']) + 2 * resolution]
    zlim = [min(voxels['ZData']) - 2 * resolution, max(voxels['ZData']) + 2 * resolution]

    return xlim, ylim, zlim


