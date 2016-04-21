# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from ramasse import *

ramasse = Ramasse()

ramasse.position = (600,400)
ramasse.obstacles = [] #[(500,800)]
ramasse.cibles = [(200,1500)] #(800,500), (10,1600),

chemin = []
for i in range(600):
    chemin.append(ramasse.position)
    ramasse.strategie()
    ramasse.position = ramasse.objectif

X = []
Y = []
for v in chemin :
    X.append(v[0])
    Y.append(v[1])

plt.plot(X,Y)
plt.plot([0,0,2000,2000,0], [0,3000,3000,0,0])
plt.plot([0,200],[800,800])
plt.plot([0,200],[2200,2200])
plt.plot([750,750],[900,2100])
plt.plot([750,1350], [1500,1500])

#plt.plot([500],[800], 'or')
plt.plot([200],[1500], 'og')
#plt.plot([10],[1600], 'og')

#plt.axis([-50,3050,-50,3050])
plt.axis("equal")

plt.show()