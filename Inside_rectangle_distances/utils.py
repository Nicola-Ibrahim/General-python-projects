from core import Point, Line, Rectangle

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