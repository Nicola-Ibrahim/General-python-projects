from core import Point, Line, Rectangle
import math


def make_rectangle(points: list[Point]):
    """Create a new rectangle from passed points

    Args:
        points (list[Point]): points of the corners of the rectangle

    Returns:
        rectangle: a Rectangle instance
    """
    # Sorting the points
    sorted_points = sorted(points)

    # Get the bottom_left point and upper_right point
    bottom_left_point, upper_right_point = Point(
        *sorted_points[0]), Point(*sorted_points[-1])

    return Rectangle(bottom_left_point, upper_right_point)


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
        return None


def calculate_distance(point1: Point, point2: Point) -> float:
    """Calculate the Euclidean distance between two points

    Args:
        point1 (Point): first point
        point2 (Point): second point

    Returns:
        float: distance value
    """
    dist = math.dist((point1.x, point1.y), (point2.x, point2.y))
    return dist


# TODO: create wrapper method for decoration
def intersected_line(line: Line, rectangle: Rectangle, 
    checking_point: Point = None, inner_point: Point = None) -> Line:

    """Intersect the line with rectangle's lines

    Args:
        line (Line): the desired line to find its intersection points
        rectangle (Rectangle): rectangle
        checking_point (Point, optional): outer line's point. Defaults to Point | None.

    Returns:
        Line: the section of line that lie inside of the rectangle
    """

    # List to hold the intersection points
    inter_points = []

    for rec_line in rectangle.lines:
        x, y = intersection(line1=line, line2=rec_line)

        inter_point = Point(x, y)

        if (rectangle.is_inner(inter_point)):
            inter_points.append(inter_point)

    if (not inter_points):
        return None

    if (isinstance(checking_point, Point)):
        # Find the distance between outer point and the
        # both intersected points
        # and select the lower distance

        dist1 = calculate_distance(checking_point, inter_points[0])
        dist2 = calculate_distance(checking_point, inter_points[1])

        line = Line(*inter_points)
        if (dist1 > dist2):
            inter_points = (inner_point, inter_points[1])

        elif (dist1 < dist2):
            inter_points = (inner_point, inter_points[0])

    return Line(*inter_points)


def location(line: Line, rectangle: Rectangle) -> Line:
    """Check the line location

    Args:
        line (Line): line to be checked
        rectangle (Rectangle): rectangle that line intersects with

    Returns:
        Line: a new line the locate inside the rectangle
    """

    IS_POINT1_INNER = rectangle.is_inner(line.point1)
    IS_POINT2_INNER = rectangle.is_inner(line.point2)

    # Both line's points are inside the rectangle
    if (IS_POINT1_INNER and IS_POINT2_INNER):
        return line

    # One of the points is outside
    elif (IS_POINT1_INNER and not IS_POINT2_INNER):

        # pass outer line outer point for calculate the distance
        return intersected_line(line, rectangle, checking_point=line.point2, inner_point=line.point1)

    elif (not IS_POINT1_INNER and IS_POINT2_INNER):
        # pass outer line outer point for calculate the distance
        return intersected_line(line, rectangle, checking_point=line.point1, inner_point=line.point2)



    elif(not IS_POINT1_INNER and not IS_POINT2_INNER):
        return intersected_line(line, rectangle)


def calculate_inner_distances(lines: tuple[Line], rectangle: Rectangle) -> tuple[list[Line], float]:
    """Calculate the inner distances for the intersected lines over rectangle

    Args:
        lines (tuple[Line]): lines to be calculated its intersected parts
        rectangle (Rectangle): rectangle that contains intersected parts

    Returns:
        tuple[list[Line], float]: tuple of new inner lines and their total distance
    """

    inner_lines = [location(line, rectangle) for line in lines]

    inner_lines = [inner_line for inner_line in inner_lines if inner_line is not None]

    total_inner_distance = sum([inner_line.distance for inner_line in inner_lines])
    total_inner_distance = round(total_inner_distance, 2)
    
    return inner_lines, total_inner_distance

