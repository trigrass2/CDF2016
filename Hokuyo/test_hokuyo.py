__author__ = 'anthony'

from time import sleep
from SerialCom import HokuyoCom, find_ports
from math import ceil
from Graph import *
from pygame import QUIT

# Find the Hokuyo
ports = find_ports()
lidar = HokuyoCom(ports[0])
sleep(0.2)

graph = Graph(size=[800,800], scale = 1/10.0)

done = False
while not done:
    for event in graph.getEvent():
        if event.type == QUIT:
            done = True

    # get clean data
    [ranging, angles] = lidar.get_fresh_data()
    [rangingC, anglesC] = lidar.clean_data(ranging, angles)

    # Convert to cartesian coordinate
    [X, Y] = lidar.polar2cartesian(rangingC, anglesC)

    # Reset screen
    graph.clearScreen()
    # Display data
    graph.displayCart(X, Y)


graph.quit()
lidar.close()