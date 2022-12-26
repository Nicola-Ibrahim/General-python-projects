import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.lines as lines

from core import Rectangle, Line, Point


def edit_figure_lim(ax: plt.Axes, line: Line) -> plt.Axes:
    """Change the figure limitation depending on the lowest and 
    highest points of the passing line

    Args:
        ax (plt.Axes): axes to be edited 
        line (Line): line that indicates the boundary of figure

    Returns:
        plt.Axes: a new edited axes 
    """

    # Get the lowest point
    sorted_point1, sorted_point2 = sorted((line.point1, line.point2))
    xlim = ax.get_xlim()
    xlim_edit = [xlim[0] - sorted_point1.x - 1, xlim[1] + sorted_point2.x + 1]
    ax.set_xlim(xlim_edit)

    ylim = ax.get_ylim()
    ylim_edit = [ylim[0] - sorted_point1.x - 1, ylim[1] + sorted_point2.x + 1]

    ax.set_xlim(ylim_edit)

    return ax
    


def plot_rectangle(rectangle: Rectangle, ax: plt.Axes = None) -> plt.Axes:
    """Draw a rectangle

    Args:
        rectangle (Rectangle): rectangle to be drawn
        ax (plt.Axes, optional): previous created axes. Defaults to None.

    Returns:
        plt.Axes: a new created or the previous passed one
    """
    # If the axes is none then create new axes
    if (ax is None or not isinstance(ax, plt.Axes)):
        ax = plt.axes()
        ax.set_xlim(-5, 10)
        ax.set_ylim(-5, 10)

    patch = pat.Rectangle(
        rectangle.lowest_point.to_tuple(),
        width=rectangle.width,
        height=rectangle.hight,
        alpha=0.6,
    )
    ax.add_patch(patch)

    return ax


def plot_line(line: Line, ax: plt.Axes = None, color: str = None) -> plt.Axes:
    """Draw a line

    Args:
        line (Line): line to be drawn
        ax (plt.Axes, optional): previous created axes. Defaults to None.
        color (matplotlib.colors.Color | str, optional): color value . Defaults to None.

    Returns:
        plt.Axes: a new created or the previous passed one
    """
    # If the axes is none then create new axes
    if (ax is None or not isinstance(ax, plt.Axes)):
        ax = plt.axes()
        ax.set_xlim(-5, 10)
        ax.set_ylim(-5, 10)

    
    # Change limitation depending on the line point
    ax = edit_figure_lim(ax, line)


    # Change the points to split x-axes from y-axes
    x_, y_ = zip(line.point1.to_tuple(),
                line.point2.to_tuple())

    ax.add_line(lines.Line2D(x_, y_, linewidth=3, color=color))
    return ax


def plot_point(point: Point, ax: plt.Axes = None, color = None):
    """Draw a point

    Args:
        point (Point): points to plotted
        ax (plt.Axes, optional): previous created axes. Defaults to None.
        color (matplotlib.colors.Color | str, optional): color value . Defaults to None.

    Returns:
        plt.Axes: a new created or the previous passed one
    """
    # If the axes is none then create new axes
    if (ax is None or not isinstance(ax, plt.Axes)):
        ax = plt.axes()
        ax.set_xlim(-5, 10)
        ax.set_ylim(-5, 10)



    ax.scatter(point.x, point.y, linewidth=5, color=color, marker='o', label=str(point))
    return ax