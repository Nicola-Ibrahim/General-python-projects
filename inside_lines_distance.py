
"""
Calculate the distance of the inside lines that intersect with 
rectangle 
"""


# Import libraries
from dataclasses import dataclass, field


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Line:
    """Line class consists of two endpoints
    """
    point1: Point
    point2: Point

    def __str__(self) -> str:
        return f"Line(p1={self.point1}, p2={self.point2})"

    @property
    def slop(self):
        """Find the slop of the line

        Returns:
            slop_value: the slop of the line
        """
        slop_value = (self.point1.y - self.point2.y) / \
            (self.point1.x - self.point2.x)
        return slop_value

    # The standard line equation is (Ax + By = C)
    @property
    def coef(self):
        """Find line's coefficiens

        Returns:
            dict: line's coefficients
        """
        A = (self.point1.y - self.point2.y)
        B = (self.point2.x - self.point1.x)
        C = (self.point1.x*self.point2.y - self.point2.x*self.point1.y)

        coef_values = dict()
        coef_values['A'] = A
        coef_values['B'] = B
        coef_values['C'] = -C
        return coef_values


@dataclass
class Rectangle:
    """
    Class is responsible to identify a new rectangle with its
    data
    """
    lowest_point: Point
    highest_point: Point
    width: float = field(init=False)
    hight: float = field(init=False)

    def __post_init__(self):
        self.width = self.highest_point.x - self.lowest_point.x
        self.hight = self.highest_point.y - self.lowest_point.y

    @property
    def lines(self):
        """Returns the rectangle lines

        Returns:
            tuple: return the lines
        """
        width = self.width
        hight = self.hight
        line1 = Line(self.lowest_point, Point(
            self.lowest_point.x, self.lowest_point.y + hight))
        line2 = Line(self.lowest_point, Point(
            self.lowest_point.x + width, self.lowest_point.y))
        line3 = Line(self.highest_point, Point(
            self.highest_point.x, self.highest_point.y - hight))
        line4 = Line(self.highest_point, Point(
            self.highest_point.x - width, self.highest_point.y))

        return (line1, line2, line3, line4)


def intersection(line1: Line, line2: Line):
    """Find the intersection point between two lines

    Args:
        line1 (Line): first passed line
        line2 (Line): second passed line

    Returns:
        Point: return the intersection point if it exists else return None
    """
    D = line1.coef['A'] * line2.coef['B'] - line1.coef['B'] * line2.coef['A']
    Dx = line1.coef['C'] * line2.coef['B'] - line1.coef['B'] * line2.coef['C']
    Dy = line1.coef['A'] * line2.coef['C'] - line1.coef['C'] * line2.coef['A']
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


if __name__ == "__main__":

    # Testing data
    rectangle_points = (
        (-2, -1),
        (-2, 5),
        (8, -1),
        (8, 5)
    )

    points = (
        ((-3, 4), (0, 8)),
        ((-4, 2), (2, 4)),
        ((-1, 4), (6, 0)),
        ((3, 7), (10, -1)),
    )

    # Convert lines points to Point class instances
    points = tuple(map(lambda line_point: (
        Point(*line_point[0]), Point(*line_point[1])), points))

    # Create Lines from the given points as Line class instances
    lines = list(map(lambda point: (Line(*point)), points))

    # Sorting the points
    sorted_points = sorted(rectangle_points)

    # Get the bottom_left point and upper_right point
    bottom_left_point, upper_right_point = Point(
        *sorted_points[0]), Point(*sorted_points[-1])

    rec = Rectangle(bottom_left_point, upper_right_point)

    for line in lines:
        print(line.coef)
        for rec_line in rec.lines:
            print(f"{rec_line} intersect at {intersection(line, rec_line)}")

        print("-"*50)
