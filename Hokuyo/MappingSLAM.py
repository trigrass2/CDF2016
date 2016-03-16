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
    MAP_SIZE_METERS         = 10
    LIDAR_DEVICE            = '/dev/ttyACM0'
    THRESH_DETECTION = 100

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
            x, y, theta = self.slam.getpos()

            self.bot_pos.append((x, y))
            self.bot_ori.append(theta)

    def stop(self):
        self.state = False