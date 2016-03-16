# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:22:06 2016

@author: Joris
"""

import numpy as np
from math import round, sqrt,cos,sin

def limite(self, coord):
    if coord[0]-self.r<=0: # si on est le long de la paroi gauche
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                return (self.r,self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                return (self.r, 3000-self.r)
            else:
                return  (self.r, coord[1])
        elif coord[0]+self.r>=2000: # si on est le long de la paroi droite
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                return  (2000-self.r,self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                return  (2000-self.r, 3000-self.r)
            else:
                return (2000-self.r, coord[1])
        else:
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                self.__objectif=(coord[0],self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                self.__objectif=(coord[0], 3000-self.r)
            else:
                return (coord[0], coord[1])


class Ramasse():
    def __init__(self):
        self.obst = None
        self.position = None
        self.objectif = None
        self.r=(290*sqrt(2)/2)+5


    @property
    def objectif(self):
        return self.__objectif

    @objectif.setter
    def objectif(self,coord):
        self.__objectif = limite(self, coord)


    def update(self):
        self.position = mapping.position_Ramasse
        self.obst = capteurs.distances, mapping.obstacles #TODO

    def strategie(self):
        score_max=0
        R=self.r
        for alpha in range(360):
            coord=R*cos(alpha),R*sin(alpha)
            point=limite(self, coord)
            score=0
            for obst in self.obst:
                d_obst=sqrt((obst[0]-point[0])**2 + (obst[1]-point[1])**2)
                score -= 1/d_obst





            if score > score_max: score_max = score




    def stop_tout(self):
        #Arrete les actionneurs et les moteurs
        pass

    def deploie_parasol(self):
        #chepaki au boulot
        pass

