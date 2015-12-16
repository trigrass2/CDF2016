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

    def displayCloud(self, points, color, size, width):
        for k in range(len(points[0])):
            x = int((points[0][k]-1000)*self.scale+self.size[0]/2)
            y = int((points[1][k]+1500)*self.scale+self.size[1]/2)
            if x < self.size[0] and y < self.size[1] and x >= 0 and y >= 0:
                pygame.draw.circle(self.screen, color, [x, y], size, width)

    def displayMap(self, map):
        # Display point cloud
        points = [map.cloud[0] + map.bot_pos[-1][0], map.cloud[1] + map.bot_pos[-1][1]]
        self.displayCloud(points, [0, 255, 0], 1, 0)

        #Display beacon
        b = map.BEACON[:]
        self.displayCloud(b.transpose(), [255,0,0], 6, 2)

        #Display robot
        bot = [[map.bot_pos[-1][0]], [map.bot_pos[-1][1]]]
        self.displayCloud(bot, [0,0,255], 5, 0)

        #Display obstacles
        obs = [[map.obstacles[i].center[0] + map.bot_pos[-1][0] for i in range(len(map.obstacles))],[map.obstacles[i].center[1] + map.bot_pos[-1][1] for i in range(len(map.obstacles))]]
        self.displayCloud(obs, [0,255,255], 3, 0)

    def show(self, i = 0):
        pygame.display.flip()
        #pygame.image.save(self.screen, "images/image%d.png"%i)
        self.clock.tick(60)

    def clearScreen(self):
        self.screen.fill(self.backgroundColor)

    def getEvent(self):
        return pygame.event.get()

    def quit(self):
        pygame.quit()