from core import Point, Line, Rectangle



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

def intersected_line(line: Line, rectangle: Rectangle, inner_point = Point|None) -> Line:
    """Intersect the line with rectangle's lines

    Args:
        line (Line): the desired line to find its intersection points
        rectangle (Rectangle): rectangle
        inner_point (Point, optional): one of the inner line's points. Defaults to Point | None.

    Returns:
        Line: the section of line that lie inside of the rectangle
    """

    # List to hold the intersection points
    inter_points = []

    for rec_line in rectangle.lines:
        x, y = intersection(line1=line, line2=rec_line)

        inter_point = Point(x, y)

        if(rectangle.is_inner(inter_point)):
            inter_points.append(inter_point)

    if(not inter_points):
        return None

    if(isinstance(inner_point, Point)):
        # Find the distance between inner point and the
        # both intersected points
        # and select the bigger distance

        # TODO: change the way of checking the actual line

        line = Line(*inter_points)
        if(line.slop > 0):
            return Line(inter_points[0], inner_point)
        
        elif(line.slop < 0):
            return Line(inter_points[1], inner_point)
    
    return Line(*inter_points)



def location(line: Line, rectangle: Rectangle):

    point1_COND = rectangle.is_inner(line.point1)
    point2_COND = rectangle.is_inner(line.point2)
    
    # Both line's points are inside the rectangle
    if(point1_COND and point2_COND):
        return line

    # One of the points is outside
    elif(point1_COND and not point2_COND):
        return intersected_line(line, rectangle, inner_point=line.point1)

    elif(not point1_COND and point2_COND):
        return intersected_line(line, rectangle, inner_point=line.point2)

    # Both are outside
    return intersected_line(line, rectangle)


