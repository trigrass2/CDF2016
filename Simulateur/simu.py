#!/usr/bin/python3.4

'''
Pour le moment, le simu se resume a un petit carre qui avance, recule, tourne quand on appuie sur les fleches du clavier

A faire (plutot vite):
-collisions
-capteurs
'''

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygon, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.initGui()

	def initGui(self):
		self.shape = QPolygon(4)
		self.shape.setPoints(240,240,270,240,270,270,240,270)
		self.shape = QPolygonF(self.shape)


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

	def keyPressEvent(self, e):
		p0 = self.shape.at(0)
		p2 = self.shape.at(2)

		if e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
			p1 = self.shape.at(1)

			if e.key() == Qt.Key_Up:
				fact = 1
			else:
				fact = -1

			#on determine le vecteur de translation a partir des coord du centre et du milieu du trait avant du carre
			x0 = (abs(p0.x() - p2.x())/2 + min((p0.x(), p2.x())))
			y0 = (abs(p0.y() - p2.y())/2 + min((p0.y(), p2.y())))

			x1 = abs(p0.x() - p1.x())/2 + min((p0.x(), p1.x()))
			y1 = (abs(p0.y() - p1.y())/2 + min((p0.y(), p1.y())))

			pas = 3#en pixel
			norme = np.sqrt((x1-x0)**2 + (y1-y0)**2)
			v_t = (fact*(x1-x0)*pas/norme, fact*(y1-y0)*pas/norme)
			Trans = np.array([[1,0,v_t[0]],[0,1,v_t[1]]])#matrice de translation

			for i in range(4):
				point = self.shape.at(i)
				pt = np.array([[point.x()],[point.y()],[1]])
				new_point = np.dot(Trans, pt)

				self.shape.replace(i, QPointF(new_point[0], new_point[1]))

		elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Right:
			#recuperer les coord du centre de rotation
			x0 = (abs(p0.x() - p2.x())/2 + min((p0.x(), p2.x())))
			y0 = (abs(p0.y() - p2.y())/2 + min((p0.y(), p2.y())))

			#definir la matrice de rotation
			if e.key() == Qt.Key_Right:
				theta = np.pi/8
			else:
				theta = -np.pi/8

			Rot = np.array([[np.cos(theta),-np.sin(theta)], [np.sin(theta), np.cos(theta)]])

			#appliquer la rotation a l'ensemble des points
			for i in range(4):
				point = self.shape.at(i)
				pt = np.array([[point.x()-x0],[point.y()-y0]])
				new_point = np.dot(Rot, pt)

				#mettre a jour les points
				self.shape.replace(i, QPointF(new_point[0]+x0, new_point[1]+y0))

		#mettre a jour la scene
		self.update()

	def drawPol(self, qp):
		qp.setPen(QColor(0,0,255))
		qp.setBrush(QColor(255,0,0))
		qp.drawConvexPolygon(self.shape)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = Window()

	sys.exit(app.exec_())
