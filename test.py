import numpy as np
import plotly.graph_objects as go
from skimage.measure import marching_cubes

def showsurface(voxels):
    """
    SHOWSURFACE: Render a surface based on voxel data using Plotly.

    Parameters:
    voxels (dict): Voxel data containing:
                   - 'XData': X coordinates of voxels.
                   - 'YData': Y coordinates of voxels.
                   - 'ZData': Z coordinates of voxels.
                   - 'Value': Values at each voxel.
                   - 'Resolution': Grid resolution.

    Returns:
    plotly.graph_objects.Figure: A Plotly figure object.
    """

    # Get unique coordinates in each dimension
    ux = np.unique(voxels['XData'])
    uy = np.unique(voxels['YData'])
    uz = np.unique(voxels['ZData'])

    # Expand the grid by one step in each direction
    resolution = voxels['Resolution']
    ux = np.concatenate([[ux[0] - resolution], ux, [ux[-1] + resolution]])
    uy = np.concatenate([[uy[0] - resolution], uy, [uy[-1] + resolution]])
    uz = np.concatenate([[uz[0] - resolution], uz, [uz[-1] + resolution]])

    # Create a grid
    X, Y, Z = np.meshgrid(ux, uy, uz, indexing='ij')

    # Create an empty voxel grid and populate it with values
    V = np.zeros(X.shape, dtype=np.float32)
    for x, y, z, value in zip(voxels['XData'], voxels['YData'], voxels['ZData'], voxels['Value']):
        ix = np.where(ux == x)[0][0]
        iy = np.where(uy == y)[0][0]
        iz = np.where(uz == z)[0][0]
        V[iy, ix, iz] = value
    #verts, faces, normals, _ = marching_cubes(V, level=0.5, spacing=(resolution, resolution, resolution))

    # Create the isosurface plot using Plotly
    fig = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=V.flatten(),
        isomin=0.5,
        isomax=1.0,  # Assuming values are normalized
        caps=dict(x_show=False, y_show=False, z_show=False),
        opacity=0.6,
        colorscale="Viridis",
    ))

    # Add axis labels and layout
    fig.update_layout(
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="data"
        ),
        title="3D Isosurface",
    )

    # Show the plot
    fig.show()

    # Return the Plotly figure for further use if needed
    return fig


# Example Usage
if __name__ == "__main__":
    # Mock voxel data
    voxels = {
        'XData': np.random.randint(0, 10, size=100),
        'YData': np.random.randint(0, 10, size=100),
        'ZData': np.random.randint(0, 10, size=100),
        'Value': np.random.choice([0, 1], size=100),
        'Resolution': 1
    }

    # Call the function
    fig = showsurface(voxels)
