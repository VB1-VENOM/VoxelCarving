# import numpy as np
# from skimage.measure import marching_cubes
# import plotly.graph_objects as go

# def showsurface(voxels, ax=None):
#     """
#     SHOWSURFACE: Draw a surface based on voxel data and return patch information.

#     Parameters:
#     voxels (dict): Voxel data containing 'XData', 'YData', 'ZData', and 'Value'.
#     ax (matplotlib.axes._subplots.Axes3DSubplot, optional): The 3D axes to plot on.

#     Returns:
#     dict: A dictionary representing the patch object, with keys:
#           'Vertices' (numpy.ndarray): The 3D coordinates of the vertices.
#           'Faces': (numpy.ndarray): The faces of the isosurface.
#           'Normals': (numpy.ndarray): Normals of the vertices.
#     """
#     # Get unique voxel coordinates
#     ux = np.unique(voxels['XData'])
#     uy = np.unique(voxels['YData'])
#     uz = np.unique(voxels['ZData'])

#     # Expand the grid by one step in each direction
#     resolution = voxels['Resolution']
#     ux = np.concatenate([[ux[0] - resolution], ux, [ux[-1] + resolution]])
#     uy = np.concatenate([[uy[0] - resolution], uy, [uy[-1] + resolution]])
#     uz = np.concatenate([[uz[0] - resolution], uz, [uz[-1] + resolution]])

#     # Create a grid
#     X, Y, Z = np.meshgrid(ux, uy, uz, indexing='ij')

#     # Create an empty voxel grid and populate it with normalized values
#     V = np.zeros(X.shape, dtype=np.float32)
#     values = np.array(voxels['Value'], dtype=np.float32)
#     # Normalize voxel values to [0, 1]
#     if values.max() > values.min():  # Avoid divide-by-zero
#         values = (values - values.min()) / (values.max() - values.min())
#     else:
#         values[:] = 1.0  # If all values are the same, set to 1

#     for x, y, z, value in zip(voxels['XData'], voxels['YData'], voxels['ZData'], values):
#         ix = np.where(ux == x)[0][0]
#         iy = np.where(uy == y)[0][0]
#         iz = np.where(uz == z)[0][0]
#         if ix < V.shape[1] and iy < V.shape[0] and iz < V.shape[2]:
#             V[iy, ix, iz] = value

#     # Create the isosurface plot using Plotly
#     fig = go.Figure(data=go.Isosurface(
#     x=X.flatten(),
#     y=Y.flatten(),
#     z=Z.flatten(),
#     value=V.flatten(),
#     isomin=V.min() + 0.1,  # Adjust based on the range
#     isomax=V.max(),
#     caps=dict(x_show=False, y_show=False, z_show=False),
#     opacity=0.6,
#     colorscale="Viridis",
# ))


#     # Add axis labels and layout
#     fig.update_layout(
#         width=1200,  # Increase width (in pixels)
#         height=800,
#         autosize=False,
#         scene=dict(
#             xaxis_title="X",
#             yaxis_title="Y",
#             zaxis_title="Z",
#             xaxis=dict(range=[ux[0], ux[-1]]),
#             yaxis=dict(range=[uy[0], uy[-1]]),
#             zaxis=dict(range=[uz[0], uz[-1]]),
#             aspectmode="data",
#             aspectratio=dict(x=1, y=1, z=1)
#         ),
#         title="3D Isosurface",
#     )

#     # Show the plot
#     fig.show()

#     # Use marching_cubes for extracting isosurface vertices, faces, and normals
#     verts, faces, normals, _ = marching_cubes(V, level=0.5, spacing=(resolution, resolution, resolution))

#     return {
#         'Vertices': verts,
#         'Faces': faces,
#         'Normals': normals
#     }

import numpy as np
from skimage.measure import marching_cubes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def showsurface(voxels,ax=None):
    """
    Draw a surface based on voxel data and return patch information.

    Parameters:
    voxels (dict): Voxel data containing 'XData', 'YData', 'ZData', 'Value', and 'Resolution'.

    Returns:
    dict: A dictionary containing the patch information:
          - 'Vertices': Coordinates of the vertices of the isosurface.
          - 'Faces': Faces of the isosurface.
          - 'Normals': Normals of the vertices.
    """
    # Get unique voxel coordinates
    ux = np.unique(voxels['XData'])
    uy = np.unique(voxels['YData'])
    uz = np.unique(voxels['ZData'])

    # Expand the model by one step in each direction
    resolution = voxels['Resolution']
    ux = np.concatenate([[ux[0] - resolution], ux, [ux[-1] + resolution]])
    uy = np.concatenate([[uy[0] - resolution], uy, [uy[-1] + resolution]])
    uz = np.concatenate([[uz[0] - resolution], uz, [uz[-1] + resolution]])

    # Create a 3D grid
    X, Y, Z = np.meshgrid(ux, uy, uz, indexing='ij')

    # Create an empty voxel grid and populate it with values
    V = np.zeros(max(X.shape,Y.shape,Z.shape), dtype=np.float32)
    for x, y, z, value in zip(voxels['XData'], voxels['YData'], voxels['ZData'], voxels['Value']):
        ix = np.where(ux == x)[0][0]
        iy = np.where(uy == y)[0][0]
        iz = np.where(uz == z)[0][0]
        if ix < V.shape[1] and iy < V.shape[0] and iz < V.shape[2]:
            V[iy, ix, iz] = value

    #Create the isosurface plot using Plotly
    fig = go.Figure(data=go.Isosurface(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=V.flatten(),
    isomin=V.min() + 0.1,  # Adjust based on the range
    isomax=V.max(),
    caps=dict(x_show=False, y_show=False, z_show=False),
    opacity=0.6,
    colorscale="Viridis",
))


    # Add axis labels and layout
    fig.update_layout(
        width=1200,  # Increase width (in pixels)
        height=800,
        autosize=False,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            xaxis=dict(range=[ux[0], ux[-1]]),
            yaxis=dict(range=[uy[0], uy[-1]]),
            zaxis=dict(range=[uz[0], uz[-1]]),
            aspectmode="data",
            aspectratio=dict(x=1, y=1, z=1)
        ),
        title="3D Isosurface",
    )

    # Show the plot
    fig.show()

    # Use marching_cubes for extracting isosurface vertices, faces, and normals
    verts, faces, normals, _ = marching_cubes(V, level=0.5, spacing=(resolution, resolution, resolution))

    return {
        'Vertices': verts,
        'Faces': faces,
        'Normals': normals
    }
