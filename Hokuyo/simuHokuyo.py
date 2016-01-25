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

def getHokuyoData(botPos, botAngle, obstacles):
    botAngle = -botAngle
    theta = minTheta
    dtheta = (maxTheta-minTheta)/N
    result = []
    while theta < maxTheta:
        D = 4000
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

    for i in range(200, 2500, 100):

        R = getHokuyoData(np.array([1000, 200]), i/50*np.pi/180, beacon)

        R = Tools.polar2cartesian(R)
        gr = Graph.Graph()
        gr.displayCloud(R, [0, 255, 0], 2, 0)
        gr.show()
