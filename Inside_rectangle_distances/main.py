
"""
Calculate the distance of the inside lines that intersect with 
rectangle 
"""

from core import Point, Line, Rectangle
from utils import make_rectangle, intersection


def process(lines: tuple[Line], rectangle: Rectangle):

    new_lines = []
    for ind, line in enumerate(lines, 1):
        # print(line.coef)
        # print(f"Line {ind} -> intersect with:")
        # for rec_line in rectangle.lines:
        #     print(f"{'':<5}{rec_line} at {intersection(line, rec_line)}")

        # print("-"*50)

        # Check line's points location
        # rectangle.lowest_point.x <= line.point1.x <= rectangle.lowest_point.x + rectangle.width

        # If both points are inside then no need to find the intersection
        if(line.point1 <= rectangle.lowest_point):
            print("yes")

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

    process(lines, rectangle)

    


