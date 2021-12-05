from typing import List, Tuple

from pyquaternion import Quaternion

Axis = Tuple[int, int, int]
Point = Tuple[int, int, int]


# this takes in the list of connections in 2d and outputs which
# axis each cube attaches through in 3d
def initialize_parameters(directions: List[int]) -> List[Axis]:
    axis = []
    for d in directions:
        if 0 == d:
            axis.append((1, 0, 0))  # positive x
        elif 1 == d:
            axis.append((0, 1, 0))  # positive y
        elif 2 == d:
            axis.append((-1, 0, 0))  # negative x
        elif 3 == d:
            axis.append((0, -1, 0))  # negative y
    return axis


# takes in the list of axis each cube attaches through and outputs where the cubes are in 3d coordinates
# 0,0,0 is the coordinate of the cube at the start of the chain
def calculate_points(axis: List[Axis]) -> List[Point]:
    points = [(0, 0, 0)]
    for a in axis:
        points.append(calculate_next_cube_point(points[-1], a))
    return points


# calculates the position of the next cube
def calculate_next_cube_point(point: Point, axis: Axis) -> Point:
    return point[0] + axis[0], point[1] + axis[1], point[2] + axis[2]


# If you look at the picture puzzle_flattened.jpeg,
# this array goes 0,0,1,0 because the cubes go out the top, top, right, top, ...
block_axis = initialize_parameters([0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0])
