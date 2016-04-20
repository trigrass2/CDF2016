#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'anthony'

import numpy as np
from threading import Thread

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel

from breezylidar import URG04LX as Lidar

MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = '/dev/ttyACM0'

class Map(Thread):

    MAP_SIZE_PIXELS         = 500
    MAP_SIZE_METERS         = 3
    LIDAR_DEVICE            = '/dev/ttyACM0'
    THRESH_DETECTION = 100

    RAW_ANGLE = -np.pi/4
    LIDAR_POS = np.array([140, 140])

    state = True

    def __init__(self, rob_start = np.array([1000, 200])):
        Thread.__init__(self)
        self.lidar = Lidar(LIDAR_DEVICE)
        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        self.N = 0
        self.bot_pos = []
        self.bot_ori = []
        self.ROB_START = rob_start

    def run(self):
        # Constant
        R = np.array([[np.cos(self.RAW_ANGLE), -np.sin(self.RAW_ANGLE)],
                      [np.sin(self.RAW_ANGLE), np.cos(self.RAW_ANGLE)]])
        lidar_dist = np.linalg.norm(self.LIDAR_POS)
        while(self.state):
            # Update SLAM with current Lidar scan
            self.scan = self.lidar.getScan()
            self.slam.update(self.scan)

            # Get current robot position
            y, x, theta = self.slam.getpos()

            x-=5000
            y-=5000
            pos = np.array([x, y])  # Position of lidar in the coordinate system from lidar
            pos = R.dot(pos)  # Orientation corrected
            pos = pos + self.ROB_START + self.LIDAR_POS  # Position of lidar in the coordinate system from map

            angle = self.RAW_ANGLE + theta*np.pi/180.0
            pos = pos - lidar_dist*np.array([np.cos(angle), np.sin(angle)])

            self.bot_pos.append(pos)
            self.bot_ori.append(theta*np.pi/180.0)

            # Find obstacles
            min_angle =-np.pi*3/4
            max_angle = np.pi*3/4
            angle = range(min_angle, max_angle, ((max_angle-min_angle)%(2*np.pi))/len(self.scan))
            polars = np.array([angle, self.scan])
            cart = polar2cartesian(polars)


    def stop(self):
        self.state = False

def polar2cartesian(polars):
    cart = polars[1] * [np.cos(polars[0]), np.sin(polars[0])]
    return cart

def find_obstacles(data):

    # Find the distance between each consecutive points.
    d_xy = data[:,1:len(data[0])] - data[:,0:len(data[0])-1]

    # Calcul de la distance
    ranges = np.linalg.norm(d_xy, axis=0)

    # Creation of the first obstacle
    obstacles=[]
    if(len(data) != 0):
        obstacles.append(Obstacle())
        obstacles[-1].append(data[:,0])

    # Process every points
    for k in range(1, len(ranges)+1):

        # If the point is to far away from the current obstacle, create a new one.
        if abs(ranges[k-1]) > Map.THRESH_DETECTION:
            obstacles.append(Obstacle())

        # Add current point to the last known obstacle
        obstacles[-1].append(item=data[:,k])

    # Find the data for the obstacles given their points.
    for obstacle in obstacles:
        obstacle.reduce()

    # Return the tab of obstacles.
    return obstacles


class Obstacle():

    TYPE_UNKNOWN = 0
    TYPE_CUBE = 1
    TYPE_ROUND = 2
    TYPE_ROBOT = 3
    TYPE_MAP = 4

    def __init__(self):
        self.center = None
        self.pointList = []
        self.size = 0
        self.type = 0

    def append(self, item):
        self.pointList.append(item)

    def reduce(self):
        self.pointList = np.array([[self.pointList[k][0] for k in range(len(self.pointList))],
                                   [self.pointList[k][1] for k in range(len(self.pointList))]])
        self.center = self.pointList.mean(1)
        self.size = np.linalg.norm(np.array([self.pointList[-1][0]-self.pointList[0][0],
                                             self.pointList[-1][1]-self.pointList[0][1]]))
        if self.size < 110:

            self.type = Obstacle.TYPE_CUBE



    def get_pos(self):
        return self.center

def is_right(points):
    vec = np.array([[points[k][0] for k in range(len(points))],
                    [points[k][1] for k in range(len(points))]])
    cen = vec.mean(1)
    dp = vec-cen
    d = [np.linalg.norm(np.array([dp[0][k], dp[1][k]])) for k in range(len(points))]