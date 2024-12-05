import numpy as np

def project(camera, world_X, world_Y, world_Z):
    """
    PROJECT: project a 3D point into an image.

    Parameters:
    camera (dict): A dictionary containing the camera's projection matrix `rawP`.
    world_X, world_Y, world_Z (numpy.ndarray): Arrays of 3D world coordinates.

    Returns:
    tuple: (im_x, im_y) arrays of projected 2D image coordinates.
    """
    # Calculate z (denominator of projection)
    z = (camera['rawP'][2, 0] * world_X +
         camera['rawP'][2, 1] * world_Y +
         camera['rawP'][2, 2] * world_Z +
         camera['rawP'][2, 3])
    
    # Calculate im_y
    im_y = np.round((
        camera['rawP'][1, 0] * world_X +
        camera['rawP'][1, 1] * world_Y +
        camera['rawP'][1, 2] * world_Z +
        camera['rawP'][1, 3]
    ) / z).astype(int)
    
    # Calculate im_x
    im_x = np.round((
        camera['rawP'][0, 0] * world_X +
        camera['rawP'][0, 1] * world_Y +
        camera['rawP'][0, 2] * world_Z +
        camera['rawP'][0, 3]
    ) / z).astype(int)

    return im_x, im_y
