import numpy as np

def decomposeP(P):
    """
    DECOMPOSEP: Decompose a projection matrix into internal and external parameters.

    Parameters:
    P (numpy.ndarray): A 3x4 projection matrix.

    Returns:
    tuple: (K, R, t) where
           - K is the 3x3 internal camera parameter matrix,
           - R is the 3x3 rotation matrix,
           - t is the 3x1 translation vector.
    """
    # Perform QR decomposition on the inverse of the first 3x3 block of P
    q, r = np.linalg.qr(np.linalg.inv(P[:3, :3]))
    invK = r[:3, :3]
    R = np.linalg.inv(q)

    # Ensure R is a proper rotation matrix with a determinant of 1
    if np.linalg.det(R) < 0:
        R = -R
        invK = -invK

    # Compute the camera intrinsic matrix K
    K = np.linalg.inv(invK)

    # Compute the translation vector t
    t = np.dot(invK, P[:, 3])

    return K, R, t
