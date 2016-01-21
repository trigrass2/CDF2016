#!/usr/bin/python
# Filename: Tools.py

__author__ = 'anthony'

import numpy as np

def isIn(pos, board):
    """ Renvoie si oui ou non une position est dans un polygone
    :param pos:
        [int, int]
    :param board:
        [coord, coord, coord, ...], coord = [int, int]
    :return:
        True : la position est contenu dans le polygone,
        False : la position est exterieur au polygone
    """
    # Some smart algorithm (See: https://en.wikipedia.org/wiki/Point_in_polygon)
    intersect = 0
    boardLen = len(board)
    for k in range(boardLen):
        if((board[k][1] < pos[1] and board[(k+1)%boardLen][1] >= pos[1]) or
           (board[k][1] > pos[1] and board[(k+1)%boardLen][1] <= pos[1])):
            if((pos[0]-board[k][0]) > (pos[1]-board[k][1])*(board[(k+1)%boardLen][0]-board[k][0])/(board[(k+1)%boardLen][1]-board[k][1])):
                intersect += 1
    if(intersect%2 == 0):
        return False
    else:
        return True

def rotate(array, angle):
    """ Renvoie une liste de points tourné d'un angle
    :param array: [coord, coord, coord, ...], coord = [int, int]
    :param angle: int
    :return: [coord, coord, coord, ...], coord = [int, int]
    """
    rotated_array = []
    for k in range(len(array)):
        rotated_array.append([array[k][0]*np.cos(angle) - array[k][1]*np.sin(angle), array[k][0]*np.sin(angle) + array[k][1]*np.cos(angle)])
    return rotated_array

def shift_relative(tab, pos):
    """ Translate le tableau d'un vecteur données
    :param tab: [coord, coord, coord, ...], coord = [int, int]
    :param pos: [int, int]
    :return: [coord, coord, coord, ...], coord = [int, int]
    """
    shifted = []
    for k in range(len(tab)):
        shifted.append([tab[k][0]+pos[0], tab[k][1]+pos[1]])
    return shifted

def extend(board, padding):
    """ Agrandi le polygone
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
        if(board[k][0] < bar[0]):
            x = board[k][0] - padding
        else:
            x = board[k][0] + padding
        # If the corner is on the left of the barycentre subtract, else add.
        if(board[k][1] < bar[1]):
            y = board[k][1] - padding
        else:
            y = board[k][1] + padding
        # Add the extended corner to the board
        ex_board.append([x, y])

    # Return the extended board
    return ex_board

def barycentre(board):
    """ Calcul de le barycentre d'un polygone
    :param board: [coord, coord, coord, ...], coord = [int, int]
    :return: [int, int]
    """
    bar = [0, 0]
    for k in range(len(board)):
        bar = [bar[0]+board[k][0], bar[1]+board[k][1]]
    bar = [bar[0]/len(board), bar[1]/len(board)]
    return bar

def polar2cartesian(angle, ranging):
    """ Converti des coordonnées polaires en coordonnées carthésiennes
    :param angle: [double, double, double, ...]
    :param ranging: [int, int, int, ...]
    :return: [X, Y], X = [int, int, int, ...], Y = [int, int, int, ...]
    """
    x = ranging * np.cos(angle+np.pi/2)
    y = ranging * np.sin(angle+np.pi/2)
    return [x,y]

# End of Tools.py