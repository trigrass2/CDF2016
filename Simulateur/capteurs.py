#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QPointF

from Objects import Cone
import numpy as np

class Sonar():
	def __init__(self, anchorPoint, heading, R):
		self.rayon = R

		self.poly = Cone(anchorPoint, heading, R)

	def update(self, anchorPoint, heading):
		self.poly.shape.replace(0, QPointF(anchorPoint.x(),anchorPoint.y()))


		x1 = anchorPoint.x() + np.cos(heading*np.pi/180)
		y1 = anchorPoint.y() + np.sin(heading*np.pi/180)

		norme = np.sqrt((x1 - anchorPoint.x()) ** 2 + (y1 - anchorPoint.y()) ** 2)

		vect_trans = ((x1 - anchorPoint.x())*self.rayon / norme,
		              (y1 - anchorPoint.y())*self.rayon / norme)


		Trans = np.array([[1, 0, vect_trans[0]],
		                  [0, 1, vect_trans[1]]])  # matrice de translation
		
		#Dessin de la nouvelle figure et suppression de l'autre
		for i in range(1, self.poly.nbp):
			point = anchorPoint
			pt = np.array([[point.x()], [point.y()], [1]])
			new_point = np.dot(Trans, pt)
			self.poly.shape.replace(i, QPointF(new_point[0], new_point[1]))

		x0 = anchorPoint.x()
		y0 = anchorPoint.y()

		signe = 1

		for i in range(1,self.poly.nbp):
			# definir la matrice de rotation
			theta = signe*np.pi/8
			Rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

			point = self.poly.shape.at(i)
			pt = np.array([[point.x() - x0], [point.y() - y0]])
			new_point = np.dot(Rot, pt)
			self.poly.shape.replace(i, QPointF(new_point[0] + x0, new_point[1] + y0))
			signe = -1
