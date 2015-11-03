__author__ = 'anthony'

from threading import Thread
import numpy as np

import Tools

class Mapping(Thread):

    THRESH_DETECTION = 0.1
    BOARD = [[0,0], [0,5], [10,5], [10,0]]

    def __init__(self, hokuyo_com, data_center):
        Thread.__init__(self)
        self.hokuyo = hokuyo_com
        self.data_center = data_center
        self.started = False
        self.data = None
        self.bot_pos = None
        self.bot_orient = None

    def stop(self):
        self.started = False

    def run(self):
        self.started = True
        while self.started:

            # Get new data from Hokuyo
            self.data = self.hokuyo.get_fresh_data()
            self.data = self.hokuyo.clean_data(self.data[0], self.data[1])
            self.data = self.hokuyo.polar2cartesian(self.data[0], self.data[1])

            # Find obstacles
            raw_obstacles = self.find_obstacles(self.data)

            # Remove obstacle outside the board
            self.obstacles = self.filter_obstacles(raw_obstacles, Mapping.BOARD, self.bot_pos[-1], self.bot_orient[-1])


    def find_positions_in_data(self):

        # Find the distance between each consecutive points.
        d_x = np.array(self.data[0][1:]) - np.array(self.data[0][:-1])
        d_y = np.array(self.data[1][1:]) - np.array(self.data[1][:-1])
        ranges = [np.linalg.norm([d_x[k], d_y[k]]) for k in range(len(d_x))]  # Calcul de la distance

        # Creation of the first obstacle
        if(len(self.data[0]) != 0):
            obstacles = [Obstacle()]
            obstacles[-1].append([self.data[0][0], self.data[1][0]])

        # Process every points
        for k in range(len(ranges)):
            # If the point is to far away from the current obstacle, create a new one.
            if ranges[k] > Mapping.THRESH_DETECTION:
                obstacles.append(Obstacle())
            # Add current point to the last known obstacle
            obstacles[-1].append(item=[self.data[0][k + 1], self.data[1][k + 1]])

        # Find the data for the obstacles given their points.
        for obstacle in obstacles:
            obstacle.reduce()

        # Return the tab of obstacles.
        return obstacles

    def filter_obstacles(raw_obstacles, board, bot_pos, bot_orien):
        # Initialize the tab of obstacle
        obstacles = []

        # Expend the board to compensate for deplacement of the robot
        extended_board = Tools.extend(board)

        # Move the board so that the robot coordinate are (0,0)
        extended_board = Tools.shift_relative(extended_board, bot_pos)

        # Rotate the board depending of the last orientation of the robot
        # -bot_orien is because we want to rotate the board relative to the robot
        extended_board = Tools.rotate(extended_board, -bot_orien)

        # Filter obstacles
        for k in range(len(raw_obstacles)):
            # Only keep the obstacle if it is in the board
            if(Tools.isIn(extended_board, raw_obstacles[k])):
                obstacles.append(raw_obstacles[k])

        # Return filtered obstacles
        return obstacles

class Obstacle():
    TYPE_LINE = 0
    TYPE_ROUND = 1
    TYPE_UNKNOWN = 3

    def __init__(self):
        self.center = None
        self.pointList = []
        self.type = None

    def append(self, item):
        self.pointList.append(item)

    def reduce(self):
        # En gros, calcul du barycentre, et définition du type en fonction du rapport (distmin/distmax)
        # distX = distX au barycentre
        self.pointList = np.matrixlib.matrix([[self.pointList[k][0] for k in range(len(self.pointList))],
                                              [self.pointList[k][1] for k in range(len(self.pointList))]])
        self.center = self.pointList.mean(1)
        self.type = Obstacle.TYPE_ROUND

        '''
        dp = (self.pointList - self.center).getA()  # matrice des vecteurs (colonne) ecart au barycentre
        r = [np.array([dp[0][k], dp[1][k]]) for k in range(dp.shape[1])]  # liste des vecteurs ecart
        d = [np.linalg.norm(w) > 0.1 for w in r]  # array des distances au barycentre
        if True in d:
            self.type = Obstacle.TYPE_LINE
        else:
            self.type = Obstacle.TYPE_ROUND
        '''

    def get_pos(self):
        return self.center