import numpy as np

def getcameradirection(camera):
    """
    GETCAMERADIRECTION: Return the view direction of a camera.

    Parameters:
    camera (dict): A dictionary containing:
                   - 'Image': The camera image as a NumPy array.
                   - 'K': The intrinsic matrix of the camera.
                   - 'R': The rotation matrix of the camera.

    Returns:
    numpy.ndarray: A unit vector representing the camera's principal axis direction.
    """
    # Center point in image coordinates
    x = np.array([
        camera['Image'].shape[1] / 2,  # Width center
        camera['Image'].shape[0] / 2,  # Height center
        1.0                            # Homogeneous coordinate
    ])

    # Transform to normalized image coordinates
    X = np.linalg.inv(camera['K']).dot(x)

    # Transform to world coordinates
    X = camera['R'].T.dot(X)

    # Normalize to unit vector
    dirn = X / np.linalg.norm(X)

    return dirn
