from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class SimuObject:

    def __init__(self,movable):
        self.movable = movable
        #TODO


class Shape():
	def __init__(self, nbp, list_of_points):
		self.shape = QPolygonF(nbp)
		for i in range(nbp):
			pt = list_of_points[i]
			self.shape.replace(i, QPointF(pt[0], pt[1]))
		self.nbp = nbp

class Cube(SimuObject):

    def __init__(self, size, x, y): #Pour l'instant x et y sont inutiles
        super().__init__(True)
        self.size = size
        self.x = x
        self.y = y
        self.shape = Shape(3, [(0,0), (20,20), (0,20)])

        #TODO

class Robot(SimuObject):

    def __init__(self, x, y): #Pour l'instant x et y sont inutiles
        super().__init__(True)
        self.size = 30
        self.x = 255
        self.y = 255
        self.shape = Shape(4, [(self.x - self.size/2, self.x - self.size/2),
                               (self.x + self.size/2, self.x - self.size/2),
                               (self.x + self.size/2, self.x + self.size/2),
                               (self.x - self.size/2, self.x + self.size/2)])

    pass
