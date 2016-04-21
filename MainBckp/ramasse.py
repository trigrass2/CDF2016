# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 18:22:06 2016

@author: Joris
"""

import numpy as np
from math import sqrt,cos,sin, exp

def limite(r, coord):
    if coord is None:
        return None
    if coord[0]-r<=0: # si on est le long de la paroi gauche
        if coord[1]-r<=0: # si on est le long de la paroi basse
            return (r,r)
        elif coord[1]+r>=3000: # si on est le long de la paroi haute
            return (r, 3000-r)
        else:
            return (r, coord[1])
    elif coord[0]+r>=2000: # si on est le long de la paroi droite
        if coord[1]-r<=0: # si on est le long de la paroi basse
            return  (2000-r,r)
        elif coord[1]+r>=3000: # si on est le long de la paroi haute
            return (2000-r, 3000-r)
        else:
            return (2000-r, coord[1])
    else:
        if coord[1]-r<=0: # si on est le long de la paroi basse
            return (coord[0],r)
        elif coord[1]+r>=3000: # si on est le long de la paroi haute
            return (coord[0], 3000-r)
        else:
            return (coord[0], coord[1])

     # if coord[0] - r <= 200:
     #     if coord[1] # il faut avoir ramasse.position
     #     return (coord[0]


class Ramasse():
    def __init__(self):
        self.r = (290*sqrt(2)/2)+5
        self.position = None
        self.objectif = None
        self.cibles = None
        self.obstacles = None
        self.murs = [(i,800) for i in range(0,201,20)] + [(i, 2200) for i in range(0,201,20)] + \
                [(750,i) for i in range(900,2101,20)] + [(i, 1500) for i in range(750, 1351,20)]


    @property
    def objectif(self):
        return self.__objectif

    @objectif.setter
    def objectif(self,coord):
        self.__objectif = limite(self.r, coord)


    def update(self):
        self.position = mapping.position_Ramasse
        self.obstacles = mapping.position_obst
        self.cibles = mapping.position_cibles

    def strategie(self):
        dist = np.inf
        for c in self.cibles:
            d_cible=sqrt((c[0]-self.position[0])**2 + (c[1]-self.position[1])**2)
            if d_cible<dist:
                dist=d_cible
                obj=c

        score_max=-np.inf
        R=self.r
        for alpha in range(0,360,5):
            coord=(R*cos(alpha) + self.position[0],R*sin(alpha) + self.position[1])
            point=limite(self.r, coord)
            score=0
            for obst in self.obstacles:
                d_obst=sqrt((obst[0]-point[0])**2 + (obst[1]-point[1])**2)
                score -= 1/(d_obst**1)
            d_cible = sqrt((obj[0]-point[0])**2 + (obj[1]-point[1])**2)
            score += d_cible**(-1)
                # if obj == (1000,2500):
                #     score += 1/d_cibles * 5
            for m in self.murs:
                d_murs = sqrt((m[0]-point[0])**2 + (m[1]-point[1])**2)
                score -= d_murs**-2 # * 1/len(self.murs)

            if score > score_max:
                score_max = score
                self.objectif = point



    def stop_tout(self):
        #Arrete les actionneurs et les moteurs
        pass

    def deploie_parasol(self):
        #chepaki au boulot
        pass

