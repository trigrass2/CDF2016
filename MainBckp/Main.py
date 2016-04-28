# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:45:24 2016

@author: Joris
"""

from ramasse import Ramasse, distance #YEAH
import time

if __name__ == "__main__":

    ramasse = Ramasse("poissons droite")

    deb = time.time()
    fin = deb + 90

    t = deb

    while t < fin:

        """
        capteurs.distances renvoie une liste contenant les distances des
        obstacles renvoyés par les capteurs.
        mapping.obstacles donne la liste des centres des robots.
        """

        ramasse.update()

        for ennemi in ramasse.obstacles: #Evitement de robots.
            if distance(ennemi, ramasse.position) <= 600: #Si un robot adverse est à moins de 60 cm, on s'arrête et on attend.
                ramasse.stop_tout()
                while distance(ennemi, ramasse.position) <= 600 :
                    ramasse.update()
                    if time.time() >= fin - 0.1 :
                        break

        if distance(ramasse.position, ramasse.liste_cibles[i]) < 20:
            for action in ramasse.liste_choses_a_faire :
                if time.time() >= fin - 0.1:
                    break
                action()
            ramasse.indice_cible += 1
            if ramasse.indice_cible >= len(ramasse.liste_cibles):
                ramasse.indice_cible = 3

        if time.time() < fin - 0.1 :
            ramasse.avance(ramasse.liste_cibles[ramasse.indice_cible])

        t = time.time()

    ramasse.stop_tout()
    ramasse.deploie_parasol()
