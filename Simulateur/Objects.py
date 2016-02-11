#!/usr/bin/python3.4

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF


class GhostShape():

    def __init__(self, nbp, list_of_points):
        self.shape = QPolygonF(nbp)
        for i in range(nbp):
            pt = list_of_points[i]
            self.shape.replace(i, QPointF(pt[0], pt[1]))
        self.nbp = nbp

class SimuObject():

    def __init__(self, movable, mass, x, y, heading, list_of_points):

        #Propriétés de l'objet
        self.movable = movable
        self.mass = mass
        self.x = x
        self.y = y
        self.heading = heading

        nbp = len(list_of_points)

        #Propriétés de la représentation graphique
        self.shape = QPolygonF(nbp)
        for i in range(nbp):
            pt = list_of_points[i]
            self.shape.replace(i, QPointF(pt[0], pt[1]))
        self.nbp = nbp #nombre de points dans l'objet



class Cube(SimuObject):
    def __init__(self, size, x, y, heading):  # Pour l'instant x et y sont inutiles

        self.size = 10

        mass = 1
        list_of_points = [(x - self.size/2, y - self.size/2),
                          (x - self.size/2, y + self.size/2),
                          (x + self.size/2, y + self.size/2),
                          (x + self.size/2, y - self.size/2)]

        super().__init__(True, mass, x, y, heading, list_of_points)


class Robot(SimuObject):
    def __init__(self, x, y, heading):  # Pour l'instant x et y sont inutiles

        self.size = 30

        mass = 10
        list_of_points = [(x - self.size / 2, y - self.size / 2),
                          (x - self.size / 2, y + self.size / 2),
                          (x + self.size / 2, y + self.size / 2),
                          (x + self.size / 2, y - self.size / 2)]

        super().__init__(True, mass, x, y, heading, list_of_points)
