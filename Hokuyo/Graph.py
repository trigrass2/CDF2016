__author__ = 'anthony'

import matplotlib.pyplot as plt
import numpy
import Tools

class Graph():

    ROBOT_SHAPE = numpy.array([[100, -100], [0, 100], [-100, -100]])

    def __init__(self):
        plt.figure(0, dpi=200)
        plt.ion()
        plt.show()


    def displayObstacles(self, obstacles):

        for k in range(len(obstacles)):
                plt.plot([int(obstacles[k].center[0]*self.scale+self.size[0]/2),
                             int(obstacles[k].center[1]*self.scale+self.size[1]/2)],
                            'g.')


    def displayCloud(self, points, color):
        plt.clf()
        plt.axis([-4000, 4000, -4000, 4000])
        plt.plot(points[0],points[1], color)


    def displayMap(self, map):
        """ Display the map
        :param map: Map() object to be displayed
        """
        # Display point cloud
        points = Tools.rotate(map.cloud, map.bot_ori[-1])
        points = Tools.translate(points, map.bot_pos[-1])
        self.displayCloud(points, '.b')

        #Display beacon
        b = map.BEACON
        self.displayCloud(b, 'Hr')

        #Display robot

        bot = Tools.rotate(self.ROBOT_SHAPE, map.bot_ori[-1]) + numpy.array([map.bot_pos[-1][0], map.bot_pos[-1][1]])

        plt.plot(bot.astype(int).transpose()[0], bot.astype(int).transpose()[1])
        plt.plot(map.bot_pos[-1][0], map.bot_pos[-1][1], '.b')

        #Display obstacles
        obs = [map.obstacles[i].center for i in range(len(map.obstacles))]
        obs = Tools.rotate(obs,  map.bot_ori[-1])
        obs = Tools.translate(obs, map.bot_pos[-1])
        self.displayCloud(obs, '*k')

    def show(self):
        plt.draw()

    def clearScreen(self):
        """ Reset the screen showing only the background
        """
        plt.clf()
        plt.axis([-4000, 4000, -4000, 4000])
