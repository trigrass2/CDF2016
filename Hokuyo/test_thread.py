from Hokuyo.Graph import *
from Hokuyo.SerialCom import HokuyoCom, find_ports
from Hokuyo.Tools import polar2cartesian

import numpy as np
from time import sleep, clock
from multiprocessing import Process, Array

def update_hokuyo(com, dataAngle, dataRange):
    last = clock()
    while 1:
        tmp = clock()
        print(tmp - last)
        last = tmp
        [ranging, angles] = com.get_fresh_data()
        angles, ranges = com.clean_data(ranging, angles)
        for i in range(len(angles)): # copy values in shared memory
            dataAngle[i] = angles[i]
            dataRange[i] = ranges[i]
        for i in range(len(angles), 1000):
            dataRange[i] = -1

if __name__ == "__main__":
    dataAngle = Array('d', 1000)
    dataRange = Array('i', 1000)
    dataRange[0] = -1

    graph = Graph()

    ports = find_ports()
    print(ports)
    com = HokuyoCom(ports[0])
    sleep(0.2)

    thread = Process(target=update_hokuyo, args=(com, dataAngle, dataRange))
    thread.start()

    for i in range(1000):
        j = 0
        while dataRange[j] >= 0:
            j = j+1
        data = np.vstack((np.array([dataAngle[0:j]]), np.array([dataRange[0:j]])))
        data = polar2cartesian(np.array(data))

        #graph.clearScreen()
        graph.displayCloud(data, color='.b')
        graph.show()
