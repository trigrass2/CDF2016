__author__ = 'anthony'

import pygame
import numpy

class Graph():
    pygame.init()

    def __init__(self, size = [409, 409], scale = 1/20.0, backgroundColor = [0,0,0], dotColor=[0,255,0]):
        # Save size parameter
        self.size = size
        self.scale = scale
        # Save color parameters
        self.backgroundColor = backgroundColor
        self.dotColor = dotColor
        # Init sceen
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.backgroundColor)
        # Init clock
        self.clock = pygame.time.Clock()

    def displayCart(self, X, Y):
        # Display Hokuyo position
        pygame.draw.circle(self.screen, [255,0,0], [int(self.size[0]/2), int(self.size[0]/2)], 5)
        # Verify tab size
        if( len(X) != len(Y)):
            print("Error: Invalid Data")
        else:
            for k in range(len(X)):
                pygame.draw.circle(self.screen, self.dotColor, [int(X[k]*self.scale+self.size[0]/2), int(Y[k]*self.scale+self.size[1]/2)], 1)


    def displayObstacles(self, obstacles, color, size):
        for k in range(len(obstacles)):
                pygame.draw.circle(self.screen, color, [int(obstacles[k].center[0]*self.scale+self.size[0]/2), int(obstacles[k].center[1]*self.scale+self.size[1]/2)], size)

    def show(self):
        pygame.display.flip()
        self.clock.tick(60)

    def clearScreen(self):
        self.screen.fill(self.backgroundColor)

    def getEvent(self):
        return pygame.event.get()

    def quit(self):
        pygame.quit()