#!/usr/bin/python3.4

'''
Pour le moment, le simu se resume a un petit carre qui avance, recule, tourne quand on appuie sur les fleches du clavier

A faire (plutot vite):
-capteurs
'''

import sys
import numpy as np
import collisions
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.initGui()

	def initGui(self):
		self.fig = Shape(4, [(240,240),(270,240),(270,270),(240,270)])
		self.pas = 3#en pixels

		#les autres figures (utiles pour les collisions)
		self.ofig = []

		self.ofig.append(Shape(3, [(35+30,40+30), (45+30,60+30), (15+30, 60+30)]))

		self.resize(500,500)
		self.center()
		self.setWindowTitle('Simulateur')
		self.show()

	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size =	self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		self.drawPol(qp)
		qp.end()

	def tryTrans(self, p0, p2, sens):
		nbp = self.fig.nbp
		virtual_fig = Shape(nbp, [(0,0) for i in range(nbp)])

		p1 = self.fig.shape.at(1)

		#on determine le vecteur de translation a partir des coord du centre et du milieu du trait avant du carre
		x0 = (abs(p0.x() - p2.x())/2 + min((p0.x(), p2.x())))
		y0 = (abs(p0.y() - p2.y())/2 + min((p0.y(), p2.y())))

		x1 = abs(p0.x() - p1.x())/2 + min((p0.x(), p1.x()))
		y1 = (abs(p0.y() - p1.y())/2 + min((p0.y(), p1.y())))

		norme = np.sqrt((x1-x0)**2 + (y1-y0)**2)
		v_t = (sens*(x1-x0)*self.pas/norme, sens*(y1-y0)*self.pas/norme)
		Trans = np.array([[1,0,v_t[0]],[0,1,v_t[1]]])#matrice de translation

		for i in range(nbp):
			point = self.fig.shape.at(i)
			pt = np.array([[point.x()],[point.y()],[1]])
			new_point = np.dot(Trans, pt)

			virtual_fig.shape.replace(i, QPointF(new_point[0], new_point[1]))

		if collisions.check_collisions(virtual_fig, self.ofig, self.geometry()):
			virtual_fig.shape.swap(self.fig.shape)

	def tryRotate(self, p0, p2, theta): # p0, p2, theta
		nbp = self.fig.nbp
		virtual_fig = Shape(nbp, [(0,0) for i in range(nbp)])

		#recuperer les coord du centre de rotation à partir du milieu de la diagonale plus la position du carré
		x0 = (abs(p0.x() - p2.x())/2 + min((p0.x(), p2.x())))
		y0 = (abs(p0.y() - p2.y())/2 + min((p0.y(), p2.y())))

		#definir la matrice de rotation
		Rot = np.array([[np.cos(theta),-np.sin(theta)], [np.sin(theta), np.cos(theta)]])

		#appliquer la rotation a l'ensemble des points
		for i in range(nbp):
			point = self.fig.shape.at(i)
			pt = np.array([[point.x()-x0],[point.y()-y0]])
			new_point = np.dot(Rot, pt)

			#mettre a jour les points
			virtual_fig.shape.replace(i, QPointF(new_point[0]+x0, new_point[1]+y0))

		if collisions.check_collisions(virtual_fig, self.ofig, self.geometry()):
			virtual_fig.shape.swap(self.fig.shape)

	def keyPressEvent(self, e):
		p0 = self.fig.shape.at(0)
		p2 = self.fig.shape.at(2)

		if e.key() == Qt.Key_Up:
			self.tryTrans( p0,p2, 1)
		elif e.key() == Qt.Key_Down:
			self.tryTrans( p0,p2, -1)
		elif e.key() == Qt.Key_Left:
			self.tryRotate( p0, p2, -np.pi/8)
		elif e.key() == Qt.Key_Right:
			self.tryRotate(p0, p2, np.pi/8)

		#mettre a jour la scene
		self.update()

	def drawPol(self, qp):
		qp.setPen(QColor(0,0,255))
		qp.setBrush(QColor(255,0,0))

		qp.drawConvexPolygon(self.fig.shape)

		for shape in self.ofig:
			qp.drawConvexPolygon(shape.shape)

class Shape():
	def __init__(self, nbp, list_of_points):
		self.shape = QPolygonF(nbp)
		for i in range(nbp):
			pt = list_of_points[i]
			self.shape.replace(i, QPointF(pt[0], pt[1]))
		self.nbp = nbp

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Window()

	sys.exit(app.exec_())
