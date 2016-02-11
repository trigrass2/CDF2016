# -*- coding: utf-8 -*-
#!/usr/bin/python3.4
"""
Created on Wed Feb 10 18:45:24 2016

@author: Joris

Python 3.4
"""

import commande #TODO script des commandes

if __name__ == "__main__":

    init() #TODO init()

    import time
    deb = time.time()
    fin = deb + 90
    t = deb

    while t < fin:
        etat = capteur(), cartographie() #TODO capteur() et cartographie()
        strategie(etat, t) #TODO strategie()

        t = time.time()
    commande.actionParasol() #TODO actionParasol()

    arretTotal() #TODO arretTotal()
