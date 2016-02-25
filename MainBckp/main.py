# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:45:24 2016

@author: Joris
"""

import Ramasse #YEAH

if __name__ == "__main__":
    
    import time
    deb = time.time()
    fin = deb + 90
    
    t = deb
    
    while t < fin:
        
        """
        capteurs.distances renvoie une liste contenant les distances des 
        obstacles renvoyés par les capteurs.
        mapping.obstacles donne la liste des centres des robots.
        """
        
        Ramasse.update()
        
        Ramasse.strategie() #TODO
        
        t = time.time()
    
    Ramasse.stop_tout()
    Ramasse.deploie_parasol()
    