#!/usr/bin/python
# Filename: Tools.py

__author__ = 'anthony'

import numpy as np

def isIn(board, pos):
    # Some smart algorithm (See: https://en.wikipedia.org/wiki/Point_in_polygon)
    intersect = 0
    boardLen = len(board)
    for k in range(boardLen):
        print(k)
        if((board[k][1] < pos[1] and board[(k+1)%boardLen][1] >= pos[1]) or
           (board[k][1] > pos[1] and board[(k+1)%boardLen][1] <= pos[1])):
            if((pos[0]-board[k][0]) > (pos[1]-board[k][1])*(board[(k+1)%boardLen][0]-board[k][0])/(board[(k+1)%boardLen][1]-board[k][1])):
                intersect += 1
    if(intersect%2 == 0):
        return False
    else:
        return True

def rotate(array, angle):
    rotated_array = []
    for k in range(len(array)):
        rotated_array.append([array[k][0]*np.cos(angle) - array[k][1]*np.sin(angle), array[k][0]*np.sin(angle) + array[k][1]*np.cos(angle)])
    return rotated_array

# Shift an array so that the pos given become the centre (0,0) of the new array
# @:param tab : table to shift
# @:param pos : pos to shift according to
def shift_relative(tab, pos):
    shifted = []
    for k in range(len(tab)):
        shifted.append([tab[k][0]-pos[0], tab[k][1]-pos[1]])
    return  shifted

def extend(board, padding):
    # Find the barycentre of the board
    bar = barycentre(board)

    # Initialize the extended board
    ex_board = []

    # Process each corner of the board
    for k in range(len(board)):
        # If the corner is bellow the barycentre subtract, else add.
        if(board[k][0] < bar[0]):
            x = board[k][0] - padding
        else:
            x = board[k][0] - padding
        # If the corner is on the left of the barycentre subtract, else add.
        if(board[k][1] < bar[1]):
            y = board[k][1] - padding
        else:
            y = board[k][1] - padding
        # Add the extended corner to the board
        ex_board.append([x, y])

    # Return the extended board
    return ex_board

def barycentre(board):
    bar = [0, 0]
    for k in range(len(board)):
        bar = [bar[0]+board[k][0], bar[1]+board[k][1]]
    bar = [bar[0]/len(board), bar[1]/len(board)]
    return bar

# End of Tools.py