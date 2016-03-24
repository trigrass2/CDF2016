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
    LIDAR_POS = np.array([140,140])

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
            scan = self.lidar.getScan()
            self.slam.update(scan)

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

    def stop(self):
        self.state = False
