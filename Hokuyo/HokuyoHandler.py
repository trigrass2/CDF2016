# -*- coding: utf8 -*-
__author__ = 'adrie_000'

from threading import Thread

import numpy as np
import numpy.matrixlib as nm


class HokuyoHandler(Thread):
    # Pourquoi ceci est un thread : parce qu'il faut que l'information donneé par l'Hokuyo soit utilisée aussi
    # fréquemment que possible. Du coup une boucle à part.

    THRESH_DETECTION = 0.1

    def __init__(self, hokuyo_com, data_center):
        Thread.__init__(self)
        self.hokuyo = hokuyo_com
        self.data_center = data_center
        self.started = False
        self.data = None

    def stop(self):
        self.started = False

    def run(self):
        self.started = True
        while self.started:
            self.data_center.recompute_orientation()
            # - lit l'hokuyo
            self.data = self.hokuyo.get_fresh_data()
            self.data = self.hokuyo.clear_data(self.data[0], self.data[1])
            self.data = self.hokuyo.polar2cartesian(self.data[0], self.data[1])
            # - Récupère la liste des nouvelles positions d'obstacles
            self.find_positions_in_data()
            # - Relie les positions avec les anciennes & stocke tout dans le data_center.
            self.relocalize()

    def find_positions_in_data(self):
        # TODO : tests
        """
        On ne se sert pas de la transformée de Hough car ici, les points sont successifs, cad ils sont déjà triés
        (Et sans vision traversante, donc des points triés par angle sont largement suffisants)
        :return:
        """
        d_x = np.array(self.data[0][1:]) - np.array(self.data[0][:-1])
        d_y = np.array(self.data[1][1:]) - np.array(self.data[1][:-1])
        ranges = [np.linalg.norm([d_x[k], d_y[k]]) for k in range(len(d_x))]  # Calcul de la distance
        # angles = [math.atan2(dY[k], dX[k]) for k in range(len(dX))]  # et de l'angle entre deux points successifs
        # Note : on a besoin de l'angle en cas de murs à angles. Sinon, cet item ne sert à rien.
        obstacles = [Obstacle()]  # Liste des points par objet discriminé
        # Ecart angulaire entre deux points : 0.35°
        # On admet que deux points appartiennent au même objet s'ils sont espacés de moins de 10cm
        obstacles[-1].append([self.data[0][0], self.data[1][0]])
        for k in range(len(ranges)):
            if ranges[k] > HokuyoHandler.THRESH_DETECTION:
                obstacles.append(Obstacle())
            obstacles[-1].append(item=[self.data[0][k + 1], self.data[1][k + 1]])
        for obstacle in obstacles:
            obstacle.reduce()
        self.data_center.obstacles = obstacles

    def relocalize(self):
        orientation = self.data_center.orientation
        # TODO
        pass


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
        self.pointList = nm.matrix([[self.pointList[k][0] for k in range(len(self.pointList))],
                                    [self.pointList[k][1] for k in range(len(self.pointList))]])
        self.center = self.pointList.mean(1)
        dp = (self.pointList - self.center).getA()  # matrice des vecteurs (colonne) ecart au barycentre
        r = [np.array([dp[0][k], dp[1][k]]) for k in range(dp.shape[1])]  # liste des vecteurs ecart
        d = [np.linalg.norm(w) > 0.1 for w in r]  # array des distances au barycentre
        if True in d:
            self.type = Obstacle.TYPE_LINE
        else:
            self.type = Obstacle.TYPE_ROUND

    def get_pos(self):
        return self.center