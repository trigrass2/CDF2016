# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from ramasse import *

ramasse = Ramasse()

ramasse.position = (800,150)
ramasse.obstacles = [(500,800)]
ramasse.cibles = [(800,500), (10,1600)]

chemin = []
for i in range(100):
    chemin.append(ramasse.position)
    ramasse.strategie()
    ramasse.position = ramasse.objectif

print(chemin)
X = []
Y = []
for v in chemin :
    X.append(v[0])
    Y.append(v[1])

plt.plot(X,Y)

plt.show()