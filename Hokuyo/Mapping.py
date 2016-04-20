#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'anthony'

import numpy as np
import Tools


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

def find_beacon(obstacles, beacons):
        nBeacon = 0
        beacon = []
        for i in range(len(beacons[0])):
            min = 400
            tmp = 0
            for obstacle in obstacles:
                if np.linalg.norm(obstacle.center - beacons[:,i]) < min:
                    min = np.linalg.norm(obstacle.center - beacons[:,i])
                    tmp = obstacle
            if tmp != 0:
                beacon.append([i, tmp.center])
                nBeacon = nBeacon + 1

        if nBeacon < 2:
            print("Error: Beacon not found!")
            beacon = 0
        return beacon


def getRobPos(beacon, bot_pos):

    pos=[]
    for i in range(0, len(beacon)-1):
        correction = 40
        distance = [correction+np.linalg.norm(beacon[0+i][1]), correction+np.linalg.norm(beacon[1+i][1])]
        coordinate = [Map.BEACON[:,beacon[0+i][0]], Map.BEACON[:,beacon[1+i][0]]]

        distance = np.array(distance)
        # Distance entre les deux bases
        a = np.sqrt((coordinate[0][0]-coordinate[1][0])**2+(coordinate[0][1]-coordinate[1][1])**2)

        # Hauteur en M du triangle forme par M et les deux bases
        h = 1/ (2*a) *\
            np.sqrt((a+distance[0]+distance[1])*(-a+distance[0]+distance[1]) *
                    (a-distance[0]+distance[1])*(a+distance[0]-distance[1]))

        # Distance entre la premiere base et H (intersection hauteur et axe des deux bases)
        d0 = np.sqrt(distance[0]**2 - h**2)

        # Vecteur directeur
        ABsurAB = np.array([[coordinate[1][0]-coordinate[0][0]], [coordinate[1][1]-coordinate[0][1]]])\
                /np.sqrt((coordinate[1][0]-coordinate[0][0])**2 + (coordinate[1][1]-coordinate[0][1])**2)
        n = np.array([ABsurAB[1], -ABsurAB[0]])

        # M position du robot
        p = np.array([[coordinate[0][0]],[coordinate[0][1]]]) + d0 * ABsurAB + h * n

        pos.append(p)

    pos.append(bot_pos)
    return np.median(np.array(pos), axis=0)

def getRobPos2(beacon_reel, beacon_found, old_pos):
    coef = 0.1
    Xt = np.ones((3,len(beacon_found)))
    X  = np.zeros((2,len(beacon_found)))
    for i in range(len(beacon_found)): # len(beacon_found)
        Xt[0, i] = beacon_found[i][1][0]
        Xt[1, i] = beacon_found[i][1][1]
        X[0, i] = beacon_reel[:,beacon_found[i][0]][0]
        X[1, i] = beacon_reel[:,beacon_found[i][0]][1]

    if len(beacon_found) == 2:
        Xt = np.append(Xt, np.array([[0],[0],[coef]]), axis=1)
        X = np.append(X, coef * old_pos, axis=1)

    Xt = Xt.transpose()
    X = X.transpose()
    tmp = (Xt.transpose()).dot(Xt)
    tmp = np.linalg.inv(tmp)
    tmp = tmp.dot(Xt.transpose())
    y = tmp.dot(X)
    pos = np.array([[y[2,0]], [y[2,1]]])
    rot = y[0:2, 0:2]
    rot = rot / np.linalg.det(rot)
    ori = -np.arctan2(rot[1][0], rot[0][0]) % (2*np.pi)
    return pos, ori


class Map:

    THRESH_DETECTION = 100
    BEACON = np.array([[0, 2000, 2000, 0], [0, 0, 3000, 3000]])

    def __init__(self, startPos, ori):
        self.N = 0
        self.bot_pos = [np.array(startPos)]
        self.bot_ori = [ori/180.0*np.pi]
        self.beacon = Map.BEACON - startPos
        self.cloud = 0
        self.obstacles = []
        self.detect = []

    def update(self, cloudMap):
        """ Update the map to the next state.
        :param cloudMap: Points list
        """
        self.cloud = cloudMap

        # Find obstacles
        self.obstacles = find_obstacles(cloudMap)

        beacon = find_beacon(self.obstacles, self.beacon)

        if beacon != 0:
            print("%d beacons found"%len(beacon))

            if len(beacon) == 2:
                # VERSION 1
                pos = getRobPos(beacon, self.bot_pos[-1])

                ori=[]
                for i in range(0, len(beacon)):
                    vecBeac = (Map.BEACON-pos)[:,beacon[0][0]] # Vecteur pointant vers la balise
                    ori0 = np.arctan2(vecBeac[1], vecBeac[0]) # Cap de la balise si ori=0
                    oriR = np.arctan2(beacon[0][1][1], beacon[0][1][0]) # Cap de la balise
                    ori.append((ori0 - oriR)%(2*np.pi))

                ori.append(self.bot_ori[-1])
                ori=np.mean(ori)

            else:
                # VERSION 2
                pos, ori = getRobPos2(Map.BEACON, beacon, self.bot_pos[-1])

            self.bot_pos.append(pos)
            self.bot_ori.append(ori)
            self.detect = [beacon[k][1] for k in range(len(beacon))]
            self.beacon = Tools.rotate(Map.BEACON - pos, -self.bot_ori[-1])

        for obstacle in self.obstacles:
            self.obstacles.center = Tools.rotate(self.obstacles.center, self.bot_ori[-1])+self.bot_pos[-1]


class Obstacle():

    def __init__(self):
        self.center = None
        self.pointList = []

    def append(self, item):
        self.pointList.append(item)

    def reduce(self):
        self.pointList = np.array([[self.pointList[k][0] for k in range(len(self.pointList))],
                                   [self.pointList[k][1] for k in range(len(self.pointList))]])
        self.center = self.pointList.mean(1)

    def get_pos(self):
        return self.center

from time import sleep
from Hokuyo.simuHokuyo import getHokuyoData
from Hokuyo.SerialCom import HokuyoCom, find_ports
import matplotlib.pyplot as plt

if __name__ == "__main__":

    #Affichage
    plt.figure(0, dpi=200)
    plt.ion()

    map = Map(np.array([[1000], [200]]), 0)
    balise = np.array([[-40, 40, 40, -40], [-40, -40, 40, 40]])
    beacon = [np.array([[0], [0]])+balise, np.array([[2000], [0   ]])+balise, np.array([[2000], [3000]])+balise, np.array([[0   ], [3000]])+balise]

    # REEL
    #ports = find_ports()
    #print(ports)
    #com = HokuyoCom(ports[0])
    #sleep(0.2)

    for i in range(180):
        '''
        # POUR LA SIMULATION

        # Hors de la boucle
        #map = Map(position initial, angle_initial)
        map = Map(np.array([[1000], [200]]), 0)

        # Dans la boucle
        #data = getHokuyoData(robot_position, angle_radian, liste d'objets, bruit)
        data = getHokuyoData([1000, 200], i*2/180.0*np.pi, beacon, 0)
        data = Tools.polar2cartesian(data)
        map.update(data)

        # Pour recuperer les données
        map.bot_ori[-1] # Dernière orientation
        map.bot_pos[-1] # Dernière position

        # FIN DE POUR LA SIMULATION
        '''


        #th = np.array([[1000], [200+100*i]])

        # REEL
        #[ranging, angles] = com.get_fresh_data()
        #data = np.array(com.clean_data(ranging, angles))
        #print(data)

        # NOT REEL
        data = getHokuyoData([1000, 200], i*2/180.0*np.pi, beacon, 0)

        # ALL
        data = Tools.polar2cartesian(data)
        plt.figure(1)
        plt.clf()
        plt.axis([-3000, 3000, -3000, 3000])
        plt.plot(data[0],data[1], "b.")

        #map.cloud = data
        map.update(data)

        # Affichage
        plt.figure(0)
        plt.clf()
        plt.axis([-1000, 3000, -1000, 4000])
        # Hokuyo
        aff = Tools.rotate(map.cloud, map.bot_ori[-1]) + map.bot_pos[-1]
        plt.plot(aff[0],aff[1], "b.")
        # Robot
        plt.plot(map.bot_pos[-1][0], map.bot_pos[-1][1], 'r^')
        # Balise reel
        for bal in beacon:
            plt.plot(bal[0], bal[1], 'g')
        # Balise detect
        for bal in map.detect:
            tmp = np.array([[bal[0]],[bal[1]]])
            tmp = Tools.rotate(tmp, map.bot_ori[-1]) + map.bot_pos[-1]
            plt.plot(tmp[0], tmp[1], 'b*')

        # Actualise
        plt.draw()

        #print("Position theorique: \n", th)
        #print("Position detecte: \n", map.bot_pos[-1])
        print("Delta Angle: ", map.bot_ori[-1]*180/np.pi)
        #sleep(0.5)
