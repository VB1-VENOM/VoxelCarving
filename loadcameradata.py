import os
import numpy as np
from scipy.io import loadmat
from skimage.io import imread
from tqdm import tqdm
from decomposeP import decomposeP
from mat4py import loadmat


def loadcameradata(data_dir, idx=None):
    """
    LOADCAMERADATA: Load the dinosaur data.

    Parameters:
    data_dir (str): Path to the directory containing the data files.
    idx (list, optional): List of indices of files to load. If None, loads all indices (1-36).

    Returns:
    list: A list of dictionaries, where each dictionary represents a camera.
    """
    if idx is None:
        idx = range(1, 37)  # Default indices 1 to 36

    # Initialize cameras as an empty list
    cameras = []

    # Load the raw P matrices
    rawP_path = os.path.join(data_dir, 'dino_Ps.mat')
    rawP_data = loadmat(rawP_path)['P']  # Assuming 'P' is the key in the MAT file
    rawP_data = np.array(rawP_data)
    #print(rawP_data)
    # Loop through the specified indices
    for i in tqdm(idx, desc="Loading images"):
        # Try to find the image file
        jpg_filename = os.path.join(data_dir, f'viff.{i:03d}.jpg')
        ppm_filename = os.path.join(data_dir, f'viff.{i:03d}.ppm')

        if os.path.exists(jpg_filename):
            filename = jpg_filename
        elif os.path.exists(ppm_filename):
            filename = ppm_filename
        else:
            raise FileNotFoundError(
                f"Could not find image {i} ('viff.{i:03d}.jpg' or 'viff.{i:03d}.ppm')."
            )

        # Decompose the projection matrix
        P_matrix = rawP_data[i-1]  # Assuming MATLAB index 1-based to Python 0-based
        #print(P_matrix.shape)
        #print(P_matrix)
        K, R, t = decomposeP(P_matrix)

        # Normalize K
        K /= K[2, 2]

        # Camera position
        T = -np.dot(R.T, t)
        # Read the image
        image = imread(filename)

        # Append the camera data to the list
        cameras.append({
            'rawP': P_matrix,
            'P': P_matrix,
            'K': K,
            'R': R,
            'T': T,
            'Image': image,
            'Silhouette': None
        })

    return cameras