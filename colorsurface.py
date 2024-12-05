import numpy as np

from project import project
from getcameradirection import getcameradirection
def colorsurface(ptch, cameras):
    """
    COLORSURFACE: color a surface based on image data.

    Parameters:
    ptch (dict): A dictionary representing the patch object, with keys:
                 'Vertices' (numpy.ndarray): The 3D coordinates of the vertices.
                 'VertexNormals' (numpy.ndarray): Normals of the vertices.
    cameras (list): A list of camera dictionaries, each with:
                    - 'Image': The image data (numpy.ndarray).
                    - Required methods for projection and camera direction.
    """
    # Validate input
    if 'Vertices' not in ptch or 'Normals' not in ptch:
        raise ValueError("First argument must contain 'Vertices' and 'VertexNormals'.")

    vertices = ptch['Vertices']
    normals = ptch['Normals']
    num_vertices = vertices.shape[0]

    # Get the view vector for each camera
    num_cameras = len(cameras)
    cam_normals = np.zeros((3, num_cameras))
    for i in range(num_cameras):
        cam_normals[:, i] = getcameradirection(cameras[i])

    # Initialize vertex color data
    vertexcdata = np.zeros((num_vertices, 3))

    # For each vertex, determine the best camera and color the vertex
    for i in range(num_vertices):
        # Compute dot product between vertex normal and camera normals
        angles = np.dot(normals[i, :], cam_normals) / np.linalg.norm(normals[i, :])
        cam_idx = np.argmin(angles)  # Select the best camera based on angle

        # Project the vertex into the chosen camera
        imx, imy = project(cameras[cam_idx], vertices[i, 0], vertices[i, 1], vertices[i, 2])

        # Map the image pixel value to the vertex color
        vertexcdata[i, :] = cameras[cam_idx]['Image'][round(imy), round(imx), :] / 255.0

    # Update patch with vertex color data
    ptch['FaceVertexCData'] = vertexcdata
    ptch['FaceColor'] = 'interp'

    return ptch