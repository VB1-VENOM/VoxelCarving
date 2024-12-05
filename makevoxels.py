import numpy as np

def makevoxels(xlim, ylim, zlim, N):
    """
    MAKEVOXELS: Create a basic grid of voxels ready for carving.

    Parameters:
    xlim (tuple): The x-axis limits as (xmin, xmax).
    ylim (tuple): The y-axis limits as (ymin, ymax).
    zlim (tuple): The z-axis limits as (zmin, zmax).
    N (int): Approximate total number of voxels.

    Returns:
    dict: A dictionary containing voxel data:
          - 'Resolution': The voxel size.
          - 'XData', 'YData', 'ZData': The 3D coordinates of the voxels.
          - 'Value': An array initialized to 1 for all voxels.
    """
    # Calculate volume of the bounding box
    volume = (xlim[1] - xlim[0]) * (ylim[1] - ylim[0]) * (zlim[1] - zlim[0])

    # Calculate voxel resolution to achieve approximately N voxels
    resolution = (volume / N) ** (1 / 3)

    # Create voxel grid
    x = np.arange(xlim[0], xlim[1] + resolution, resolution)
    y = np.arange(ylim[0], ylim[1] + resolution, resolution)
    z = np.arange(zlim[0], zlim[1] + resolution, resolution)

    # Create 3D meshgrid
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Flatten the grid to create voxel coordinates
    XData = X.flatten()
    YData = Y.flatten()
    ZData = Z.flatten()

    # Initialize voxel values to 1
    Value = np.ones_like(XData, dtype=np.float32)

    # Return voxel data as a dictionary
    return {
        'Resolution': resolution,
        'XData': XData,
        'YData': YData,
        'ZData': ZData,
        'Value': Value
    }
