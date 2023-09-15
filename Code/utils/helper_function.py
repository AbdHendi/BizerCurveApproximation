import numpy as np
import matplotlib.pyplot as plt
from bezier_curve_approximation.generate_curve import bezier_curve
from PIL import Image
import io


plt.rcParams["figure.figsize"] = (10, 8)


# search for the closest point
def closest_point(bezier_curve_points, point):
    """
    point: a point from sequence point, (row from numpy array)
    bezier_curve_points: curve points
    --------------------------------------------
    return index of closest point in {curve_points} to {point}
    """
    distances = np.apply_along_axis(lambda row: np.linalg.norm(row - point), 1, bezier_curve_points)
    idx = np.argmin(distances)
    # return index of closest point and the distance itself.
    return distances[idx]


def area_of_triangle(a, b, c):
    """
    calculate the area of a triangle
    a, b, c : edges of the triangle
    a: current point form the sequence poitns
    b: closest point to a.
    c: neighbor of the b point, either prev or next.

    ----------------------------------------
    return the area of the triangle and the cosine alpha
    """
    # d1 : distance between curr_point from sequence points and prev_neighbor qk-1 or next_neighbor qk+1
    d1 = np.linalg.norm(a - c)

    # d2 : distance between curr_point from sequence points and closest point qk = ||d - qk||
    d2 = np.linalg.norm(a - b)

    # d3 : distance between closest point qk and prev_neighbor qk-1 or next_neighbor qk+1
    d3 = np.linalg.norm(b - c)

    # s:  semi-perimeter = (d1 + d + d2) / 2
    s = (d1 + d2 + d2) / 2

    # area of the first triangle
    return np.sqrt(s * (s - d1) * (s - d2) * (s - d3)), np.inner(a - b, c - b)


def plot_curves(curr_solution, sequence, delta, conn2conn, im, save=False, last_component=False,
                connection_point_type='velocity'):
    if not save:
        plt.cla()
    plt.imshow(im, aspect='auto')
    plt.scatter(sequence[:, 0], sequence[:, 1], s=0.2, label='sequence points', color='black')
    prev1 = 0
    for idx in conn2conn:
        new_bc = bezier_curve(curr_solution[prev1: idx+1], delta)
        plt.scatter(curr_solution[prev1: idx+1, 0], curr_solution[prev1: idx+1, 1], label='control points', s=2,
                    color='green')
        plt.plot(new_bc[:, 0], new_bc[:, 1], 'r--', label='piecewise bezier curve', linewidth=1)
        plt.pause(0.0000000001)
        prev1 = idx
    new_bc = bezier_curve(curr_solution[prev1:], delta)
    plt.scatter(curr_solution[prev1:, 0], curr_solution[prev1:, 1], label='control points', s=2, color='green')
    plt.plot(new_bc[:, 0], new_bc[:, 1], 'r--', label='piecewise bezier curve', linewidth=1)
    plt.pause(0.0000000001)
    if last_component:
        plt.savefig('result_{}_{}.png'.format(len(sequence), connection_point_type))


