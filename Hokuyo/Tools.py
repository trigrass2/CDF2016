#!/usr/bin/python
# Filename: Tools.py

__author__ = 'anthony'

import numpy as np


def isIn(point, board):
    """ Return True if the point is inside the polygon, False otherwise
    :param point:
        [int, int]
    :param board:
        [coord, coord, coord, ...], coord = [int, int]
    :return:
        True : the point is inside the polygon,
        False : the point is outside the polygon
    """
    # Some smart algorithm (See: https://en.wikipedia.org/wiki/Point_in_polygon)
    intersect = 0
    boardLen = len(board)
    for k in range(boardLen):
        if((board[k][1] < point[1] and board[(k+1)%boardLen][1] >= point[1]) or
           (board[k][1] > point[1] and board[(k+1)%boardLen][1] <= point[1])):
            if((point[0]-board[k][0]) > (point[1]-board[k][1])*(board[(k+1)%boardLen][0]-board[k][0])/(board[(k+1)%boardLen][1]-board[k][1])):
                intersect += 1
    if intersect % 2 == 0:
        return False
    else:
        return True


def rotate(array, angle):
    """ Rotate a list of points by the given angle
    :param array: List of points
        [coord, coord, coord, ...], coord = [int, int]
    :param angle: Angle
        int
    :return: [coord, coord, coord, ...], coord = [int, int]
    """
    rotated_array = []
    for k in range(len(array)):
        rotated_array.append([array[k][0]*np.cos(angle) - array[k][1]*np.sin(angle), array[k][0]*np.sin(angle) + array[k][1]*np.cos(angle)])
    return rotated_array


def translate(tab, pos):
    """ Translate a points list by the given vector
    :param tab: Points list
        [coord, coord, coord, ...], coord = [int, int]
    :param pos: Vector
        [int, int]
    :return: [coord, coord, coord, ...], coord = [int, int]
    """
    shifted = []
    for k in range(len(tab)):
        shifted.append([tab[k][0]+pos[0], tab[k][1]+pos[1]])
    return shifted


def expend(board, padding):
    """ Expend a rectangular board
    :param board: [coord, coord, coord, ...], coord = [int, int]
    :param padding: int
    :return: [coord, coord, coord, ...], coord = [int, int]
    """
    # Find the barycentre of the board
    bar = barycentre(board)

    # Initialize the extended board
    ex_board = []

    # Process each corner of the board
    for k in range(len(board)):
        # If the corner is bellow the barycentre subtract, else add.
        if board[k][0] < bar[0]:
            x = board[k][0] - padding
        else:
            x = board[k][0] + padding
        # If the corner is on the left of the barycentre subtract, else add.
        if board[k][1] < bar[1]:
            y = board[k][1] - padding
        else:
            y = board[k][1] + padding
        # Add the extended corner to the board
        ex_board.append([x, y])

    # Return the extended board
    return ex_board


def barycentre(board):
    """ Find the barycenter of a polygon
    :param board: Points list
        [coord, coord, coord, ...], coord = [int, int]
    :return: [int, int]
    """
    bar = [0, 0]
    for k in range(len(board)):
        bar = [bar[0]+board[k][0], bar[1]+board[k][1]]
    bar = [bar[0]/len(board), bar[1]/len(board)]
    return bar


def polar2cartesian(polars):
    """ Convert polar coordinates to cartesian coordinates
    :param polars: list of polar coordinates
    :return: Points list
        [coord, coord, coord, ...]
    """
    cart = polars[:][1] * [np.cos(polars[:][0]+np.pi/2), np.sin(polars[:][0]+np.pi/2)]
    return np.transpose(cart)


def clean_data(ranges, angles, limits = [20, 4100]):
    """ Delete abnormal values
    :param ranges: [int, int, int, ...]
    :param angles: [double, double, double, ...]
    :return: [range, angle], range = [int, int, int, ...], angle = [double, double, double, ...]
    """
    ranges_cleaned = []
    angles_cleaned = []
    for k in range(len(ranges)):
        if not (ranges[k] < limits[0] or ranges[k] > limits[1]):
            ranges_cleaned.append(ranges[k])
            angles_cleaned.append(angles[k])
    return [ranges_cleaned, angles_cleaned]

# End of Tools.py