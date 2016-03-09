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
        self.r=(290*sqrt(2)/2)+5


    @property
    def objectif(self):
        return self.__objectif

    @objectif.setter
    def objectif(self,coord):
        if coord[0]-self.r<=0: # si on est le long de la paroi gauche
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                self.__objectif=(self.r,self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                self.__objectif=(self.r, 3000-self.r)
            else:
                self.__objectif = (self.r, coord[1])
        elif coord[0]+self.r>=2000: # si on est le long de la paroi droite
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                self.__objectif = (2000-self.r,self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                self.__objectif = (2000-self.r, 3000-self.r)
            else:
                self.__objectif = (2000-self.r, coord[1])
        else:
            if coord[1]-self.r<=0: # si on est le long de la paroi basse
                self.__objectif=(coord[0],self.r)
            elif coord[1]+self.r>=3000: # si on est le long de la paroi haute
                self.__objectif=(coord[0], 3000-self.r)
            else:
                self.__objectif = (coord[0], coord[1])



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

