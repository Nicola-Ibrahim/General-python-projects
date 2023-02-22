"""
Calculate the distance of the inside lines that intersect with 
rectangle 
"""

import draw
import matplotlib.pyplot as plt
import utils
from core import Line, Point, Rectangle

if __name__ == "__main__":

    # Testing data
    rectangle_points = ((-2, -1), (-2, 5), (8, -1), (8, 5))

    lines_points = (
        ((-3, 4), (0, 8)),
        ((6, 2), (12, 9)),
        ((-5, 2), (5, 9)),
        ((-4, 2), (2, 4)),
        ((-1, 4), (6, 0)),
        ((3, 7), (10, -1)),
    )

    # Convert lines points to Point class instances
    lines_points = tuple(
        map(
            lambda line_point: (Point(*line_point[0]), Point(*line_point[1])),
            lines_points,
        )
    )

    # Create Lines from the given points as Line class instances
    lines = tuple(map(lambda point: (Line(*point)), lines_points))

    rectangle = utils.make_rectangle(rectangle_points)

    inner_lines, total_inner_distance = utils.calculate_inner_distances(
        lines, rectangle
    )

    # Plot rectangle
    ax = draw.plot_rectangle(rectangle)

    # Plot lines
    for line in lines:
        ax = draw.plot_line(line, ax=ax, color="black")

    # Plot inner lines
    for line in inner_lines:
        ax = draw.plot_line(line, ax=ax, color="green")

    # Change the title of the figure
    ax.set_title(label=f"The total_inner_distance is {total_inner_distance}")

    plt.legend()
    plt.show()
