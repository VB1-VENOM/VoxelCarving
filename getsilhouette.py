import numpy as np
import math
from skimage.morphology import remove_small_objects, remove_small_holes
from skimage.segmentation import clear_border

def getsilhouette(im):
    """
    GETSILHOUETTE: Find the silhouette of an object centered in the image.

    Parameters:
    im (numpy.ndarray): Input image as a NumPy array (height x width x channels).

    Returns:
    numpy.ndarray: Binary silhouette mask of the object.
    """
    h, w, d = im.shape

    # Initial segmentation: more red than blue
    S = im[:, :, 0] > (im[:, :, 2] - 2)

    # Remove regions touching the border or smaller than 10% of the image area
    S = clear_border(S)
    S = remove_small_objects(S, min_size=math.ceil(h * w / 10))

    # Remove holes smaller than 1% of the image area
    S = ~remove_small_objects(~S, min_size=math.ceil(h * w / 100))

    return S
