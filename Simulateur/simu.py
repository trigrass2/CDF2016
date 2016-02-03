#!/usr/bin/python3.4

"""
Pour le moment, le simu se resume a un petit carre qui avance, recule, tourne quand on appuie sur les fleches du clavier
"""
# TODO : capteurs, objets


import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

import collisions
import Objects


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initGui()

    def initGui(self):

        self.pas = 3  # en pixels

        self.allObjects = []

        self.robot = Objects.Robot(255, 255, 0)
        self.allObjects.append(self.robot)

        '''
		#les autres figures (utiles pour les collisions)
		self.ofig = []
		self.ofig.append(Shape(3, [(35+30,40+30), (45+30,60+30), (15+30, 60+30)]))
		'''

        # ajout cube
        self.cubes = []
        self.cubes.append(Objects.Cube(20, 290, 240, 0))
        self.cubes.append(Objects.Cube(20, 40, 40, 0))
        self.cubes.append(Objects.Cube(20, 40, 80, 0))


        for cube in self.cubes:
            self.allObjects.append(cube)

        self.resize(500, 500)
        self.center()
        self.setWindowTitle('Simulateur')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, event): #Override de la méthode QWidget
        qp = QPainter()
        qp.begin(self)
        self.drawPol(qp)
        qp.end()

    def tryTrans(self, movingObject, sens):

        nbp = movingObject.nbp  # nombre de points
        virtual_fig = Objects.GhostShape(nbp, [(0, 0) for i in range(nbp)])

        p0 = movingObject.shape.at(0)
        p1 = movingObject.shape.at(1)
        p2 = movingObject.shape.at(2)

        #Détermination de la liste des autres objets

        otherObjects = self.allObjects.copy()
        otherObjects.remove(movingObject)

        '''
        Test pour DEBUG

        for obj in otherObjects:
            print('x =',obj.x,'y =',obj.y)
        '''

        # on determine le vecteur de translation a partir des coord du centre et du milieu du trait avant du carre
        x0 = (abs(p0.x() - p2.x()) / 2 + min((p0.x(), p2.x())))
        y0 = (abs(p0.y() - p2.y()) / 2 + min((p0.y(), p2.y())))

        x1 = abs(p0.x() - p1.x()) / 2 + min((p0.x(), p1.x()))
        y1 = (abs(p0.y() - p1.y()) / 2 + min((p0.y(), p1.y())))

        norme = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        v_t = (sens * (x1 - x0) * self.pas / norme, sens * (y1 - y0) * self.pas / norme)
        Trans = np.array([[1, 0, v_t[0]], [0, 1, v_t[1]]])  # matrice de translation

        #Dessin de la nouvelle figure et suppression de l'autre
        for i in range(nbp):
            point = movingObject.shape.at(i)
            pt = np.array([[point.x()], [point.y()], [1]])
            new_point = np.dot(Trans, pt)

            virtual_fig.shape.replace(i, QPointF(new_point[0], new_point[1]))

        #Ckeck de la collision
        if collisions.check_collisions(virtual_fig, otherObjects, self.geometry()):
            virtual_fig.shape.swap(movingObject.shape)

    def tryRotate(self, movingObject, theta):  # p0, p2, theta
        nbp = movingObject.nbp
        virtual_fig = Objects.GhostShape(nbp, [(0, 0) for i in range(nbp)])

        p0 = movingObject.shape.at(0)
        p2 = movingObject.shape.at(2)

        #Détermination de la liste des autres objets
        otherObjects = self.allObjects.copy()
        otherObjects.remove(movingObject)

        # recuperer les coord du centre de rotation à partir du milieu de la diagonale plus la position du carré
        x0 = (abs(p0.x() - p2.x()) / 2 + min((p0.x(), p2.x())))
        y0 = (abs(p0.y() - p2.y()) / 2 + min((p0.y(), p2.y())))

        # definir la matrice de rotation
        Rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        # appliquer la rotation a l'ensemble des points
        for i in range(nbp):
            point = movingObject.shape.at(i)
            pt = np.array([[point.x() - x0], [point.y() - y0]])
            new_point = np.dot(Rot, pt)

            # mettre a jour les points
            virtual_fig.shape.replace(i, QPointF(new_point[0] + x0, new_point[1] + y0))

        if collisions.check_collisions(virtual_fig, otherObjects, self.geometry()):
            virtual_fig.shape.swap(movingObject.shape)

    def keyPressEvent(self, e): #Override de la méthode QWidget
        p0 = self.robot.shape.at(0)
        p2 = self.robot.shape.at(2)

        if e.key() == Qt.Key_Up:
            self.tryTrans( self.robot, 1)
        elif e.key() == Qt.Key_Down:
            self.tryTrans( self.robot, -1)
        elif e.key() == Qt.Key_Left:
            self.tryRotate( self.robot, -np.pi / 16)
        elif e.key() == Qt.Key_Right:
            self.tryRotate( self.robot, np.pi / 16)

        # mettre a jour la scene
        self.update()

    def drawPol(self, qp):
        qp.setPen(QColor(0, 0, 255))
        qp.setBrush(QColor(255, 0, 0))

        qp.drawConvexPolygon(self.robot.shape)

        for cube in self.cubes:
            qp.drawConvexPolygon(cube.shape)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
