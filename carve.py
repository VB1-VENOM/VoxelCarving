import numpy as np
from project import project

def carve(voxels, camera):
    """
    CARVE: Remove voxels that are not in the silhouette.

    Parameters:
    voxels (dict): A dictionary containing voxel data with keys 'XData', 'YData', 'ZData', and 'Value'.
    camera (dict): A dictionary containing camera data with keys 'Image' and 'Silhouette'.

    Returns:
    dict: Updated voxel data as a dictionary.
    """
    # Project voxel coordinates into image space
    x, y = project(camera, voxels['XData'], voxels['YData'], voxels['ZData'])

    # Get image dimensions
    h, w = camera['Image'].shape[:2]

    # Find voxels within the image bounds
    keep = np.where((x >= 1) & (x <= w) & (y >= 1) & (y <= h))[0]
    x = x[keep]
    y = y[keep]

    # Map to silhouette and find valid indices
    ind = np.ravel_multi_index(
        (np.round(y).astype(int) - 1, np.round(x).astype(int) - 1), 
        (h, w)
    )
    valid_indices = camera['Silhouette'].flat[ind] >= 1
    keep = keep[valid_indices]

    # Update the voxel dictionary with valid voxels
    updated_voxels = {
        'Resolution': voxels['Resolution'],
        'XData': voxels['XData'][keep],
        'YData': voxels['YData'][keep],
        'ZData': voxels['ZData'][keep],
        'Value': voxels['Value'][keep]
    }

    # Return the updated voxel dictionary
    #print("lol:",updated_voxels)
    return updated_voxels
