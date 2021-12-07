"""
    The methods in this file are just a way to do rotations of 0, 90, 180, or 270 degrees
    about the main axis (x, y, z) on the unit vectors along each axis.

    I found the formula in calculate_component() through trial and error.
    I verified it is correct by manually inspecting the output from main().
"""


def calculate_component(orig, direction, r):
    dir_nonzero = direction + 1
    dir_nonzero = dir_nonzero - 1 * abs(direction)  # avoids division by zero
    return (orig - r % (2 * dir_nonzero)) * (-2 * (r // 2) + 1)


def rotate_component(a, m, r, a_i):
    next_axis = (a_i + 1) % 3
    prev_axis = (a_i + 2) % 3
    if m[next_axis] != 0 and a[next_axis] == 0:
        return calculate_component(a[a_i], a[a_i] - a[prev_axis], r)
    elif m[prev_axis] != 0 and a[prev_axis] == 0:
        return calculate_component(a[a_i], a[a_i] + a[next_axis], r)
    else:
        return a[a_i]


# This version of the method avoids branching, which is necessary to avoid for the constraint programming version
# def rotate_component(a, m, r, a_i):
#     next_axis = (a_i + 1) % 3
#     prev_axis = (a_i + 2) % 3
#     enable_next = abs(m[next_axis]) * (-abs(a[next_axis]) + 1)
#     updated_next = calculate_component(a[a_i], a[a_i] - a[prev_axis], r)
#     enable_prev = abs(m[prev_axis]) * (-abs(a[prev_axis]) + 1)
#     updated_prev = calculate_component(a[a_i], a[a_i] + a[next_axis], r)
#     enable_neither = abs(enable_next + enable_prev - 1)
#     updated_neither = a[a_i]
#     return enable_next * updated_next + enable_prev * updated_prev + enable_neither * updated_neither


def rotate_a_about_m_by_r(a, m, r):
    x = rotate_component(a, m, r, 0)
    y = rotate_component(a, m, r, 1)
    z = rotate_component(a, m, r, 2)
    return x, y, z


def main():
    main_axis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    rotations = [0, 1, 2, 3]
    all_axis = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    for m in main_axis:
        for a in all_axis:
            print(f'Rotate {a} about {m}:')
            for r in rotations:
                print(f'{r}: {rotate_a_about_m_by_r(a, m, r)}')


if __name__ == '__main__':
    main()
