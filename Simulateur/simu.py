#!/usr/bin/python

import sys
import pygame  # , pylygon
from pygame.locals import *


class PosWheels():
	def __init__(self, lx, ly, posx, posy, dimx, dimy, alpha=0):
		self.lx = lx
		self.ly = ly

		self.r1 = (posx, posy + self.ly / 2)
		self.r2 = (posx + self.lx - dimx, posy + self.ly / 2)

		self.head = (posx + self.lx / 2 - dimy / 2, posy)

	def update(self, posx, posy, dimx, dimy, alpha=0):
		self.r1 = (posx, posy + self.ly / 2)
		self.r2 = (posx + self.lx - dimx, posy + self.ly / 2)

		self.head = (posx + self.lx / 2 - dimy / 2, posy)
#

def main():
	continuer = 1

	dimr = (30, 30)
	dimw = (4, 4)
	posr = (200, 200)

	posw = PosWheels(dimr[0],dimr[1], posr[0],posr[1], dimw[0], dimw[1])

	pygame.init()

	fenetre = pygame.display.set_mode((640, 480))
	fond = pygame.Surface((640, 480))
	fond.fill((255, 255, 255))

	robot = pygame.Surface(dimr)
	robot.fill((255, 0, 0))

	r1 = pygame.Surface(dimw)
	r2 = pygame.Surface(dimw)
	head = pygame.Surface(dimw)

	r1.fill((0, 0, 0))
	r2.fill((0, 0, 0))
	head.fill((0, 0, 255))

	while continuer:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				continuer = 0

		fenetre.blit(fond, (0, 0))

		fenetre.blit(robot, posr)
		fenetre.blit(r1, posw.r1)
		fenetre.blit(r2, posw.r2)
		fenetre.blit(head, posw.head)

		pygame.display.flip()


if __name__ == '__main__':
	main()