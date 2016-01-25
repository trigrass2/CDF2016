__author__ = 'anthony'

import pygame
import numpy
import Tools

class Graph():
    pygame.init()

    ROBOT_SHAPE = numpy.array([[-100, -100], [100, -100], [0, 100]])

    def __init__(self, size = [409, 409], scale = 1/20.0, backgroundColor = [0,0,0], dotColor=[0,255,0]):
        """
        :param size: Window size
            [int, int]
        :param scale: Millimeter to Pixel scale
            double
        :param backgroundColor: Background color in RGB
            [int, int, int]
        :param dotColor: Dots color in RGB
            [int, int, int]
        """

        self.size = size
        self.scale = scale
        self.backgroundColor = backgroundColor
        self.dotColor = dotColor

        # Init sceen
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.backgroundColor)

        # Init clock
        self.clock = pygame.time.Clock()


    def displayObstacles(self, obstacles, color, size):
        """ Display the obstacle as dots on the Graph
        :param obstacles: List of Obstacle() objects
        :param color: Dots color in RGB
            [int, int, int]
        :param size: Size of the dots
            int
        """

        for k in range(len(obstacles)):
                pygame.draw.circle(self.screen, color, [int(obstacles[k].center[0]*self.scale+self.size[0]/2), int(obstacles[k].center[1]*self.scale+self.size[1]/2)], size)


    def displayCloud(self, points, color, size, width):
        """ Display a cloud of points on the Graph
        :param points: List of coordinates
            [coord, coord, coord, ...], coord=[int, int]
        :param color: Circles color in RGB
            [int, int, int]
        :param size: Size of the circle in pixels
            int
        :param width: Width of circle (0 : fill the circle)
            int
        """

        for k in range(len(points)):
            x = int((points[k][0]-1000)*self.scale+self.size[0]/2)
            y = int(-(points[k][1]-1500)*self.scale+self.size[1]/2)
            if x < self.size[0] and y < self.size[1] and x >= 0 and y >= 0:
                pygame.draw.circle(self.screen, color, [x, y], size, width)

    def displayMap(self, map):
        """ Display the map
        :param map: Map() object to be displayed
        """
        # Display point cloud
        points = Tools.rotate(map.cloud, -map.bot_ori[-1])
        points = Tools.translate(points, map.bot_pos[-1])
        self.displayCloud(points, [0, 255, 0], 1, 0)

        #Display beacon
        b = map.BEACON[:]
        self.displayCloud(b, [255,0,0], 6, 2)
        #self.displayCloud(Tools.rotate(map.detect+map.bot_pos[-1], -map.bot_ori[-1]), [100,100,100], 15, 2)

        #Display robot

        bot = Tools.rotate(self.ROBOT_SHAPE, map.bot_ori[-1]) + numpy.array([map.bot_pos[-1][0], map.bot_pos[-1][1]])
        sceen_rob = ((bot-[1000, 1500])*self.scale)*numpy.array([1, -1])+numpy.array(self.size)/2

        pygame.draw.polygon(self.screen, [0, 0, 255], sceen_rob.astype(int), 2)

        #Display obstacles
        obs = [map.obstacles[i].center for i in range(len(map.obstacles))]
        obs = Tools.rotate(obs,  -map.bot_ori[-1])
        obs = Tools.translate(obs, map.bot_pos[-1])
        self.displayCloud(obs, [0, 255, 255], 3, 0)

    def show(self, filename=0):
        """ Update the display
        :param filename: Name of the file used to save the graph
        """

        pygame.display.flip()
        self.clock.tick(60)

        # Save the graph
        if filename!=0:
            pygame.image.save(self.screen, filename)


    def clearScreen(self):
        """ Reset the screen showing only the background
        """
        self.screen.fill(self.backgroundColor)

    def getEvent(self):
        """ Get the event send by pygame
        :return : pygame.event.get()
        """
        return pygame.event.get()

    def quit(self):
        """ Quit pygame
        """
        pygame.quit()