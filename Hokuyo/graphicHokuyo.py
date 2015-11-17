__author__ = 'adrie_000'

import pygame
from time import sleep
from SerialCom import HokuyoCom, find_ports
from math import ceil

ports = find_ports()
print(ports)
com = HokuyoCom('ttyACM0')
sleep(0.2)

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]

pygame.init()
size = [409, 409]
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    [ranging, angles] = com.get_fresh_data()
    print([ranging, angles])
    f = open('lidar.raw', 'w')
    f.write(str(ranging) + str(angles))
    f.close()
    screen.fill(white)
    pygame.draw.circle(screen, green, [204, 204], 205)
    [r2, ang2] = com.clear_data(ranging, angles)
    [X, Y] = com.polar2cartesian(ranging, angles)
    for k in range(len(X)):
        pygame.draw.circle(screen, red, [int(ceil(X[k]/20.0))+204, int(ceil(Y[k]/20.0))+204], 1)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
com.com.close()