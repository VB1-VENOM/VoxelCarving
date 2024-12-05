import carve
def carveall(voxels, cameras):
    """
    CARVEALL: carve away voxels using all cameras.

    Parameters:
    voxels (dict): A dictionary containing voxel data.
    cameras (list): A list of camera dictionaries, each with the required projection and silhouette data.

    Returns:
    dict: Updated voxel data after carving with all cameras.
    """
    for camera in cameras:
        voxels, _ = carve(voxels, camera)
    return voxels