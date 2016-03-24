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

    def __init__(self):
        Thread.__init__(self)
        self.lidar = Lidar(LIDAR_DEVICE)
        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        self.N = 0
        self.bot_pos = []
        self.bot_ori = []

    def run(self):
        while(self.state):
            # Update SLAM with current Lidar scan
            self.slam.update(self.lidar.getScan())

            # Get current robot position
            y, x, theta = self.slam.getpos()

            x-=5000
            y-=5000
            y-=198

            angle = self.RAW_ANGLE + theta*3.1415/180
            R = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
            pos = R.dot(np.array([x,y]))
            print(pos)

            self.bot_pos.append(pos)
            self.bot_ori.append(theta)

    def stop(self):
        self.state = False