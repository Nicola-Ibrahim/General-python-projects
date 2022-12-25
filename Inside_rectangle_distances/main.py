
"""
Calculate the distance of the inside lines that intersect with 
rectangle 
"""

from core import Point, Line, Rectangle
from utils import make_rectangle, location


def calculate_inner_distance(lines: tuple[Line], rectangle: Rectangle):

    inner_lines = [location(line, rectangle) for line in lines]

    inner_lines = [line.distance for line in lines if line is not None]
    
    return sum(inner_lines)

if __name__ == "__main__":

    # Testing data
    rectangle_points = (
        (-2, -1),
        (-2, 5),
        (8, -1),
        (8, 5)
    )

    lines_points = (
        ((-3, 4), (0, 8)),
        # ((6, 2), (12, 9)),
        ((-4, 2), (2, 4)),
        ((-1, 4), (6, 0)),
        ((3, 7), (10, -1)),
    )

    

    # Convert lines points to Point class instances
    lines_points = tuple(map(lambda line_point: (
        Point(*line_point[0]), Point(*line_point[1])), lines_points))

    # Create Lines from the given points as Line class instances
    lines = tuple(map(lambda point: (Line(*point)), lines_points))


    rectangle = make_rectangle(rectangle_points)

    print(calculate_inner_distance(lines, rectangle))

    


