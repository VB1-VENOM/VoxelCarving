def make_full_axes(axh):
    """
    MAKE_FULL_AXES: Adjust axes to fill the available space.

    Parameters:
    axh (matplotlib.axes._subplots.Axes or matplotlib.figure.Figure): 
        An Axes object to modify, or a Figure object to adjust all axes.

    Behavior:
    - If `axh` is an Axes object, the axis labels and ticks are turned off,
      and the axes fill the available space.
    - If `axh` is a Figure object, the changes are applied to all Axes in the figure.
    """
    import matplotlib.pyplot as plt

    if isinstance(axh, plt.Figure):
        # Get all axes in the figure
        axes = axh.get_axes()
    else:
        # Assume a single Axes instance
        axes = [axh]

    for ax in axes:
        # Turn off the axis labels and ticks
        ax.axis('off')

        # Adjust the axes to fill the outer position
        bbox = ax.get_position()
        ax.set_position(bbox)

        # If needed, ensure positions are clamped within [0, 1]
        pos = ax.get_position().bounds
        new_pos = (
            max(pos[0], 0),
            max(pos[1], 0),
            min(pos[2], 1),
            min(pos[3], 1),
        )
        ax.set_position(new_pos)
