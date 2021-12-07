"""
    The methods in this file have to do with the creating and manipulating the puzzle datastructures
"""

from rotate_axis import rotate_a_about_m_by_r


# Input: the flattened representation of the puzzle (as list of attachment direction in 2d - up, right, left, down)
# Output: which axis each block attaches through
# See picture 'puzzle_flattened.jpeg'
def initialize_axis(attachments):
    axis = []
    for attach in attachments:
        if 0 == attach:
            axis.append((1, 0, 0))  # positive x
        elif 1 == attach:
            axis.append((0, 1, 0))  # positive y
        elif 2 == attach:
            axis.append((-1, 0, 0))  # negative x
        elif 3 == attach:
            axis.append((0, -1, 0))  # negative y
    return axis


# See picture 'puzzle_flattened.jpeg'
real_puzzle_attachments = [0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
real_puzzle_axis = initialize_axis(real_puzzle_attachments)


def update_puzzle_axis(axis, total_rotation):
    a1 = rotate_a_about_m_by_r(axis, (1, 0, 0), total_rotation[0])
    a2 = rotate_a_about_m_by_r(a1, (0, 1, 0), total_rotation[1])
    return rotate_a_about_m_by_r(a2, (0, 0, 1), total_rotation[2])


def add_rotation(rotation, axis, prev_total):
    return (
        (prev_total[0] + axis[0] * rotation) % 4,
        (prev_total[1] + axis[1] * rotation) % 4,
        (prev_total[2] + axis[2] * rotation) % 4,
    )


# Input: the initial axis for each block and the rotation about those axis
# Output: the new axis for each block after the rotations are applied
def update_all_puzzle_axis(axis, rotations):
    # Originally this method used quaternions but I found a different way to rotate about an axis when I was working
    # on the constraint programming version of this solver
    new_axis = [axis[0]]
    total_rotation = (0, 0, 0)
    total_rotation = add_rotation(rotations[0], new_axis[0], total_rotation)
    for i in range(1, len(axis)):
        # round to the nearest int, since the quaternion rotation often gives floats that are really close to zero or 1
        new_axis.append(update_puzzle_axis(axis[i], total_rotation))
        total_rotation = add_rotation(rotations[i], new_axis[i], total_rotation)
    return new_axis


# Input: the axis each block attaches through
# Output: the location of each block in 3d coordinates. Initial block is (0,0,0).
def calculate_points(axis):
    points = [(0, 0, 0)]
    for a in axis:
        points.append(add_tuple(points[-1], a))
    return points


def add_tuple(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def subtract_tuple(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


# Input: a point
# Output: the set of adjacent points
def get_adjacent(p):
    return {
        (p[0] + 1, p[1], p[2]),
        (p[0] - 1, p[1], p[2]),
        (p[0], p[1] + 1, p[2]),
        (p[0], p[1] - 1, p[2]),
        (p[0], p[1], p[2] + 1),
        (p[0], p[1], p[2] - 1),
    }


def bounding_box(points):
    x, y, z = zip(*points)
    return (min(x), min(y), min(z)), (max(x)+1, max(y)+1, max(z)+1)


def volume(points):
    min_p, max_p = bounding_box(points)
    diff = subtract_tuple(max_p, min_p)
    return diff[0] * diff[1] * diff[2]
