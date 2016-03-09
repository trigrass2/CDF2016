# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:22:06 2016

@author: Joris
"""

import numpy as np
from math import round, sqrt

class Ramasse():
    def __init__(self):
        self.obst = None
        self.position = None
        self.objectif = None
        self.r=(25*sqrt(2)/2)+5


    @property
    def objectif(self):
        return self.objectif

    @objectif.setter
    def objectif(self,coord):
        if coord[0]-self.r<=0:
            if coord[1]-self.r<=0:
                return self.r,self.r
            elif coord[1]+self.r>=3000:
                return self.r, 3000-self.r
            else:
                return self.r, coord[1]



    def update(self):
        self.position = mapping.position_Ramasse
        self.obst = capteurs.distances, mapping.obstacles #TODO

    def strategie(self):
        #raph au boulot
        pass


    def stop_tout(self):
        #Arrete les actionneurs et les moteurs
        pass

    def deploie_parasol(self):
        #chepaki au boulot
        pass

