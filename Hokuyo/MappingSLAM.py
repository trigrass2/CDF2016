#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'anthony'

import numpy as np
from threading import Thread

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.components import URG04LX as LaserModel

from breezylidar import URG04LX as Lidar

from simuHokuyo import getHokuyoData

MAP_SIZE_PIXELS         = 1000
MAP_SIZE_METERS         = 7
LIDAR_DEVICE            = '/dev/ttyACM0'

class Map(Thread):

    MAP_SIZE_PIXELS         = 1000
    MAP_SIZE_METERS         = 7
    LIDAR_DEVICE            = '/dev/ttyACM0'
    THRESH_DETECTION = 100

    RAW_ANGLE = np.pi/4
    LIDAR_POS = np.array([140,140])



    def __init__(self):
        Thread.__init__(self)
        #self.lidar = Lidar(LIDAR_DEVICE)
        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS, map_quality=50, hole_width_mm=200, max_search_iter=10000)
        self.N = 0
        self.bot_pos = [[1500, 1300]]
        self.bot_ori = [0]
        self.state = True

    def run(self):
        self.i = 0
        x_th = 1500
        y_th = 1300

        while(self.state):
            if(self.i<10):
                y_th +=35
            elif(self.i<33):
                x_th -= 45
            elif(self.i<45):
                y_th -= 35
            else:
                y_th -= 10
                x_th += 10
            # Update SLAM with current Lidar scan
            #self.slam.update(self.lidar.getScan())
            data = getHokuyoData([x_th, y_th],
                                 -self.i*5/180.0*np.pi, [np.array([[0, 2000, 2000, 0],[0, 0, 3000, 3000]]),
                                 np.array([[650, 1350, 1350, 650],[1450, 1450, 1550, 1550]]),
                                 np.array([[1500, 1600, 1600, 1500],[1000, 1000, 1100, 1100]]),
                                 np.array([[1000+200*np.cos(k*10/180*np.pi) for k in range(0,36)],
                                           [2500+200*np.sin(k*10/180*np.pi) for k in range(0,36)]])], 0)

            list = data[1].tolist()
            if(len(list) == 682):
                self.slam.update(list, [0,0,0.1])

            # Get current robot position
            y, x, theta = self.slam.getpos()
            x-=3500
            y-=3500
            x = -x
            #y-=198
            x+=1500
            y+=1300

            #angle = self.RAW_ANGLE + theta*3.1415/180
            #R = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
            #pos = R.dot(np.array([x,y]))
            pos = np.array([x,y])

            self.bot_pos.append(pos)
            self.bot_ori.append(theta)

            self.i += 1

    def stop(self):
        self.state = False