import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def showcamera(ax, camera):
    """
    SHOWCAMERA: Draw a schematic of cameras in a 3D plot.

    Parameters:
    ax (matplotlib.axes._subplots.Axes3DSubplot): The 3D axes to plot on.
    cameras (list): A list of camera dictionaries, each containing:
                    - 'T': Camera center (translation vector).
                    - 'R': Camera rotation matrix.
                    - 'K': Camera intrinsic matrix.
                    - 'Image': Camera image as a NumPy array.
    """
    scale = 0.2
    subsample = 16
    #print("ooooo",camera,"gg")

        
    cam_t = camera['T']

    # Draw the camera center
    ax.scatter(cam_t[0], cam_t[1], cam_t[2], color='blue', s=10, label="Camera Center")

    # Image dimensions
    h, w, _ = camera['Image'].shape

    # Calculate image corners in image coordinates
    imcorners = np.array([
        [0, w, 0, w],
        [0, 0, h, h],
        [1, 1, 1, 1]
    ])

    # Back-project image corners to world coordinates
    worldcorners = iBackProject(imcorners, scale, camera)

    # Draw lines from camera center to image corners
    for i in range(4):
        iPlotLine(ax, cam_t, worldcorners[:, i], 'b-')

    # Draw the image plane
    x, y = np.meshgrid(np.arange(1, w + 1, subsample), np.arange(1, h + 1, subsample))
    pix = np.vstack((x.flatten(), y.flatten(), np.ones_like(x.flatten())))
    worldpix = iBackProject(pix, scale, camera)

    smallim = camera['Image'][::subsample, ::subsample, :]
    img_plane_x = worldpix[0, :].reshape(h // subsample, w // subsample)
    img_plane_y = worldpix[1, :].reshape(h // subsample, w // subsample)
    img_plane_z = worldpix[2, :].reshape(h // subsample, w // subsample)

    # Add the image plane as a surface
    ax.plot_surface(
        img_plane_x,
        img_plane_y,
        img_plane_z,
        rstride=1,
        cstride=1,
        facecolors=smallim / 255.0,
        shade=False
    )

    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio


def iBackProject(x, dist, camera):
    """
    IBACKPROJECT: Back-project an image location a distance DIST and return the world location.

    Parameters:
    x (numpy.ndarray): Image coordinates as a 3xN array.
    dist (float): Distance for back-projection.
    camera (dict): Camera dictionary containing 'K', 'R', and 'T'.

    Returns:
    numpy.ndarray: World coordinates as a 3xN array.
    """
    if x.shape[0] == 2:
        x = np.vstack((x, np.ones((1, x.shape[1]))))

    X = np.linalg.inv(camera['K']) @ x
    normX = np.sqrt(np.sum(X**2, axis=0))
    X = X / normX
    return camera['T'][:, None] - dist * camera['R'].T @ X


def iPlotLine(ax, x0, x1, style):
    """
    IPLOTLINE: Plot a 3D line.

    Parameters:
    ax (matplotlib.axes._subplots.Axes3DSubplot): The 3D axes to plot on.
    x0 (numpy.ndarray): Starting point of the line (3,).
    x1 (numpy.ndarray): Ending point of the line (3,).
    style (str): Line style (e.g., 'b-').
    """
    ax.plot(
        [x0[0], x1[0]],
        [x0[1], x1[1]],
        [x0[2], x1[2]],
        style[0],
        linestyle=style[1:]
    )
