#!/usr/bin/python
# Filename: Tools.py

__author__ = 'anthony'

import numpy as np


def isIn(point, board):
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
    rotation = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
    return rotation.dot(array)


def polar2cartesian(polars):
    cart = polars[1] * [np.cos(polars[0]+np.pi/2), np.sin(polars[0]+np.pi/2)]
    return cart


def clean_data(angles, ranges, limits = [20, 4100]):
    ranges_cleaned = []
    angles_cleaned = []
    for k in range(len(ranges)):
        if not (ranges[k] < limits[0] or ranges[k] > limits[1]):
            ranges_cleaned.append(ranges[k])
            angles_cleaned.append(angles[k])
    return [angles_cleaned, ranges_cleaned]

# End of Tools.py