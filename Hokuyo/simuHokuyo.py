import numpy as np

N = 240
minTheta = -3*np.pi/4
maxTheta = 3*np.pi/4

def setN(size):
    N = size
    print("N value changed.")

def setMinTheta(angle):
    minTheta = angle
    while(maxTheta < minTheta):
        maxTheta = maxTheta + 2*np.pi
    while(maxTheta - 2*np.pi > minTheta):
        maxTheta = maxTheta - 2*np.pi
    print("Min Theta value changed.")

def setMaxTheta(angle):
    maxTheta = angle
    while(maxTheta < minTheta):
        minTheta = minTheta - 2*np.pi
    while(maxTheta - 2*np.pi > minTheta):
        minTheta = minTheta + 2*np.pi
    print("Max Theta value changed.")

def getHokuyoData(botPos, botAngle, obstacles, error):
    ''' Return a liste of points in polar coordinate
    :param botPos: [double, double]
    :param botAngle: double
    :param obstacles: List of List of points
    :param error: error used to create brownian noise (in millimeters)
    :return: List of points in polar coordinates
    '''
    # Initialize variable
    cum_error = error
    botAngle = -botAngle
    theta = minTheta
    dtheta = (maxTheta-minTheta)/N

    result = []
    while theta < maxTheta:
        D = 5000
        if((theta+botAngle)%np.pi == 0):
            for obstacle in obstacles:

                for i in range(len(obstacle)):
                    if (obstacle[(i-1)][0]-botPos[0])*(obstacle[i][0]-botPos[0]) <= 0:
                        if (obstacle[i][0]-botPos[0]) != 0:
                            d = obstacle[i-1][1] - botPos[1] + (obstacle[i-1][0]-botPos[0])/(obstacle[i][0]-botPos[0]) * (obstacle[i][1]-obstacle[i-1][1])
                        else:
                            d = obstacle[i][1] - botPos[1]
                        if d<D:
                            D = d
        else:
            a = np.sin(theta + botAngle + np.pi/2)/np.cos(theta + botAngle + np.pi/2)
            b = botPos[1] - a*botPos[0]
            for obstacle in obstacles:
                for i in range(len(obstacle)):
                    dA = obstacle[i-1][0]*a+b-obstacle[i-1][1]
                    dB = obstacle[i][0]*a+b-obstacle[i][1]
                    d = np.linalg.norm(obstacle[i] - obstacle[i-1])
                    if dA*dB < 0:
                        e = d/(np.abs(dA)+np.abs(dB))*np.abs(dA)
                        M = obstacle[i-1] + (obstacle[i]-obstacle[i-1])*e/d
                        vecteur = M-botPos
                        direction = np.arctan2(vecteur[1], vecteur[0])
                        if np.linalg.norm(vecteur) < D and np.cos(theta+botAngle+np.pi/2 - direction) > 0.5:
                            D = np.linalg.norm(M-botPos)

        # Brownian noise
        cum_error = cum_error + np.random.normal(0, error)
        D = D + cum_error

        #Save distance
        if D < 4000:
            result.append([theta, D])
        theta = theta + dtheta

    if not result:
        result = [[0, 0]]

    return np.array(result).transpose()

import Tools, Graph, time
if __name__ == "__main__":
    balise = np.array([[-40, -40], [40, -40], [40, 40], [-40, 40]])
    beacon = [np.array([0, 0])+balise, np.array([2000, 0])+balise, np.array([2000, 3000])+balise, np.array([0, 3000])+balise]

    for i in range(0, 150, 1):
        data = getHokuyoData([1000, 200], 2*i/180.0*np.pi, [np.array([0, 0])+balise, np.array([2000, 0])+balise,
                                                                 np.array([2000, 3000])+balise, np.array([0, 3000])+balise], 5)

        R = Tools.polar2cartesian(data)
        gr = Graph.Graph()
        gr.displayCloud(R, [0, 255, 0], 2, 0)
        gr.show()
