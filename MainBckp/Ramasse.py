# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:22:06 2016

@author: Joris
"""

import numpy as np
from math import round

class Ramasse():
    def __init__(self):
        self.obst = None
        self.map = Map()
        self.position = None

    
    def update(self):
        self.position = mapping.position_Ramasse
        self.obst = capteurs.distances, mapping.obstacles #TODO
        self.map.updateMap(self.obst, self.position)
        
    def strategie(self):
        #raph au boulot
        pass

        
    def stop_tout(self):
        #Arrete les actionneurs et les moteurs        
        pass

    def deploie_parasol(self):
        #chepaki au boulot
        pass

class Map():
    def __init__(self):
        L=3000
        l=2000
        map=np.zeros((L/10,l/10))

    def updateMap(self, obst, pos):
        distances, obs = obst
        for d in distances:
            #todo
        for o in obs:
            x,y = o
            pos_obs = round(o)