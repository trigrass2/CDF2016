# -*- coding: utf-8 -*-

#import matplotlib.pyplot as plt
from ramasse import *

ramasse = Ramasse()

ramasse.position = (800,150)
ramasse.obstacles = [(500,800)]
ramasse.cibles = [(800,500), (10,1600)]

chemin = []
for i in range(1000):
    chemin.append(ramasse.position)
    ramasse.strategie()
    ramasse.position = ramasse.objectif
