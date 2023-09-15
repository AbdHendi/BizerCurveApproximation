import numpy as np
from utils.helper_function import closest_point
from bezier_curve_approximation.generate_curve import bezier_curve


# DetermineDiscrepancy({q},{d})
def determine_discrepancy(curve_points, sequence_points):
    """
    curve_points: piecewise bezier curve points. numpy array.
    segments_points: points was obtained from curve digitization list of numpy array
    sequence_points: input points.(numpy array)
    connection_points: list of indices of connection points from sequence points
    """
    distances = np.apply_along_axis(lambda row: closest_point(curve_points, row), 1, sequence_points)
    return np.sum(distances)


def objective_function(curve_points, sequence_points, weight):
    """
    cost function we want to minimize it.
    curve_points: piecewise bezier curve points. numpy array.
    sequence_points: input points.(numpy array)
    -------------------------
    return total error
    """

    # first term of the error function, sum of difference between sequence points and closest point to each of them.
    discrepancy = determine_discrepancy(curve_points, sequence_points)

    # second term of error function, the length of the approximation curve.
    curve_len = np.diff(curve_points, axis=0)
    curve_len = np.sum(np.sqrt((curve_len ** 2).sum(axis=1)))

    return (weight * discrepancy) + ((1 - weight) * curve_len)


def evaluate_function(control_points, sequence_points, weight, delta):
    bc = bezier_curve(control_points, delta)
    return objective_function(bc, sequence_points, weight)
