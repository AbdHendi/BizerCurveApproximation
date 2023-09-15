import numpy as np
from bezier_curve_approximation.evalute import evaluate_function
from utils.helper_function import plot_curves


def fixed_length_connection_points(sequence_point_length):
    connection_points_indices = list(range(40, sequence_point_length-20, 40))
    return connection_points_indices


def generate_initial_solution(sequence_points, connection_points_indices):
    """

    :param sequence_points: input of algorithm
    :param connection_points_indices: connection points indexes from the sequence points
    :return: initial solution (control points and connection points)
    """
    if connection_points_indices is None:
        connection_points_indices = fixed_length_connection_points(sequence_points.shape[0])
    # init 2 control points for each segment  of the curve
    size = ((len(connection_points_indices) - 1) * 2 + len(connection_points_indices)) + 6

    # Assign random values to the coordinates of control points
    random_solution = np.random.rand(size, sequence_points.shape[1])

    # Rescale the value to be in the range of input sequence point
    for i in range(sequence_points.shape[1]):
        random_solution[:, i] = random_solution[:, i] * np.max(sequence_points[:, i])

    # replace first and last points from the generated solution with first and last points from sequence points.
    random_solution[0], random_solution[-1] = sequence_points[0], sequence_points[-1]

    # connection points indices in the solution matrix
    index_of_connection_points = list(range(3, size - 1, 3))
    random_solution[index_of_connection_points] = sequence_points[connection_points_indices]
    for i in range(1, len(random_solution) - 1, 3):
        random_solution[i] = (random_solution[i - 1] * 0.2 + random_solution[i + 2] * 0.8)
        random_solution[i + 1] = (random_solution[i - 1] * 0.8 + random_solution[i + 2] * 0.2)

    # return position of initial solution
    # index_of_connection_points (connection point indices in the solution matrix)
    # connection_points_indices (connection point indices in the input sequence)
    return random_solution, index_of_connection_points, connection_points_indices


def optimization(sequence_points, connection_points_indices, delta, weight, max_iter, file):
    """

    :param img_buffer:
    :param sequence_points: 2D-numpy array represents the input of user
    :param connection_points_indices: indices of connection point in the sequence_points array
    :param delta: a hyperparameter to control the number of points generated using bizer curve function
    :param weight: The weight corresponding to the error caused by the distance and length of the generated curve
    :param max_iter: maximum iteration in algorithm
    :param file: The path of the image we want to draw on it.
    :return: 2D-array contains the coordinates of control points that minimize the total error.
    """
    # move options for continues variables
    con_var_options = [[0, 1], [1, 0], [-1, 0], [0, -1],
                       [1, 1], [1, -1], [-1, 1], [-1, -1]]

    # move option for discrete variables
    # generate initial random solution.
    curr_solution, index_of_connection_points, connection_points_indices = \
        generate_initial_solution(sequence_points, connection_points_indices)

    step_size = 15
    # error for each segment
    curr_errors = {}
    step_sizes = {}
    attempts = {}
    # evaluate each segment
    prev1, prev2 = 0, 0
    # index_of_connection_points = (connection point indices in the solution matrix)
    # connection_points_indices (connection point indices in the input sequence)
    for idx1, idx2 in zip(index_of_connection_points, connection_points_indices):
        label = '{}-{}-{}-{}'.format(prev1, idx1 + 1, prev2, idx2 + 1)
        total_error = evaluate_function(curr_solution[prev1: idx1 + 1],
                                        sequence_points[prev2: idx2 + 1], weight, delta)
        prev1 = idx1
        prev2 = idx2
        curr_errors[label] = total_error
        step_sizes[label] = step_size

    # for the last segment
    label = '{}-{}-{}-{}'.format(prev1, '0', prev2, '0')
    total_error = evaluate_function(curr_solution[prev1:],
                                    sequence_points[prev2:], weight, delta)
    curr_errors[label] = total_error
    step_sizes[label] = step_size
    step_down = 0.2
    error_to_return = 0
    # start optimization
    for _ in range(max_iter):
        enhance = False
        if len(curr_errors) <= 0: break
        # get the segment with maximum error
        segment_index = max(curr_errors, key=curr_errors.get)
        # get the start, end indices of the current segment as string
        segment_index_ = segment_index.split('-')
        # convert the indices to integers
        s1, e1, s2, e2 = int(segment_index_[0]), int(segment_index_[1]), int(segment_index_[2]), int(segment_index_[3])
        # copy the current solution
        copy_solution = np.zeros_like(curr_solution)
        copy_solution[:, :] = curr_solution[:, :]

        best_option = None

        # the current error of the segment we handle it
        lowest_error = curr_errors[segment_index]
        # choose one control point randomly to change its coordinate
        random_index = np.random.choice([1, 2])
        # for each possible direction we can move control point to it:
        for option in con_var_options:
            # try to move the control point
            copy_solution[s1 + random_index, :] = curr_solution[s1 + random_index, :] + \
                                                  (np.array(option) * step_sizes[segment_index])
            # if the segment was the last one
            if e1 == 0:
                error = evaluate_function(copy_solution[s1:, :],
                                          sequence_points[s2:, :], weight, delta)
            else:
                error = evaluate_function(copy_solution[s1:e1, :],
                                          sequence_points[s2:e2, :], weight, delta)
            # if one movement enhance the total error
            if error <= lowest_error:
                lowest_error = error
                best_option = option
        # if we had an improvement
        if best_option is not None:
            enhance = True
            # apply the change on the original solution array
            curr_solution[s1 + random_index, :] = curr_solution[s1 + random_index, :] + \
                                                  (np.array(best_option) * step_sizes[segment_index])
            # update the error of the current segment
            curr_errors[segment_index] = lowest_error
        if not enhance:
            # track the error value of the current segment to avoid stuck in local minima
            label_with_error = segment_index + "_" + "{}".format(int(lowest_error))
            # update how much this error appears
            attempts[label_with_error] = attempts.get(label_with_error, 0) + 1
            if label_with_error in attempts.keys():
                attempts[label_with_error] += 1
            else:
                attempts[label_with_error] = 1
            if step_sizes[segment_index] - step_down > 0:
                step_sizes[segment_index] -= step_down
            if label_with_error in attempts.keys() and attempts[label_with_error] > 15:
                error_to_return += curr_errors[segment_index]
                del curr_errors[segment_index]
        plot_curves(curr_solution, sequence_points, delta, index_of_connection_points, file)
        if segment_index in curr_errors.keys() and curr_errors[segment_index] < 10:
            error_to_return += curr_errors[segment_index]
            del curr_errors[segment_index]
    plot_curves(curr_solution, sequence_points, delta, index_of_connection_points, file)
    return [curr_solution, error_to_return + sum(curr_errors.values()), index_of_connection_points]
