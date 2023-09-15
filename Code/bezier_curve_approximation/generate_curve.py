import numpy as np
factorial = [1]


# find factorial using dynamic programming
def factorial_dp(n):
    global factorial
    for i in range(1, n + 1):
        factorial.append(factorial[-1] * i)


factorial_dp(20)


def bernstein_polynomial_function(n, i, u):
    global factorial
    if len(factorial) < n:
        for j in range(factorial[-1], n + 1):
            factorial.append(factorial[-1] * (factorial[-1] + 1))
    if i > n:
        i = n - i
    return (factorial[n] / (factorial[n - i] * factorial[i])) * np.power(u, i) * np.power(1 - u, n - i)


def bezier_curve(control_points, delta):
    """
    delta: refinement parameter, determine the number of points we will obtain from each segment
    control_points: control points
    ---------------------------------------------
    return list of points {q_points} represent the curve
    """
    number_of_points = control_points.shape[0]

    # parameter to control the quality of algorithm by determine the number of points from each segment.
    u = np.linspace(0.0, 1.0, int(1 / delta))
    bernstein_array = np.array(
        [bernstein_polynomial_function(n=number_of_points - 1, i=i, u=u) for i in range(number_of_points)])

    current_x = np.dot(control_points[:, 0], bernstein_array)
    current_y = np.dot(control_points[:, 1], bernstein_array)
    return np.array([current_x, current_y]).T
