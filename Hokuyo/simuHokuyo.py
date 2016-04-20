import numpy as np

N = 682
minTheta = -120*np.pi/180
maxTheta = 120*np.pi/180

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
    theta = minTheta
    dtheta = (maxTheta-minTheta)/(N-1)
    result = np.array([[1000.0],[0]])
    for i in range(0, N):
        D = 5000
        if((theta+botAngle)%np.pi == 0):
            for obstacle in obstacles:

                for i in range(len(obstacle)):
                    if (obstacle[0,i-1]-botPos[0])*(obstacle[0,i]-botPos[0]) <= 0:
                        if (obstacle[0,i]-botPos[0]) != 0:
                            d = obstacle[1,i-1] - botPos[1] + (obstacle[0,i-1]-botPos[0])/(obstacle[0,i]-botPos[0]) * (obstacle[1,i]-obstacle[1,i-1])
                        else:
                            d = obstacle[1,i] - botPos[1]
                        if d<D:
                            D = d
        else:
            a = np.sin(theta + botAngle + np.pi/2)/np.cos(theta + botAngle + np.pi/2)
            b = botPos[1] - a*botPos[0]
            for obstacle in obstacles:
                for i in range(0, len(obstacle[0])):
                    dA = obstacle[0,i-1]*a+b-obstacle[1,i-1]
                    dB = obstacle[0,i]*a+b-obstacle[1,i]
                    d = np.linalg.norm(obstacle[:,i] - obstacle[:,i-1])
                    if dA*dB < 0:
                        e = d/(np.abs(dA)+np.abs(dB))*np.abs(dA)
                        M = obstacle[:,i-1] + (obstacle[:,i]-obstacle[:,i-1])*e/d
                        vecteur = M-botPos
                        direction = np.arctan2(vecteur[1], vecteur[0])
                        if np.linalg.norm(vecteur) < D and np.cos(theta+botAngle+np.pi/2 - direction) > 0.5:
                            D = np.linalg.norm(M-botPos)

        # Brownian noise
        if error>0:
            cum_error = cum_error + np.random.normal(0, error)
        D = D + cum_error

        #Save distance
        if D < 4000:
            if result[0,0] == 1000:
                result[0,0] = theta
                result[1,0] = D
            else:
                result = np.append(result, np.array([[theta], [D]]), axis=1)
        theta = theta + dtheta

    if result[0,0] == 1000:
        result = np.array([[0], [0]])

    return result


from Tools import polar2cartesian
import matplotlib.pyplot as plt
if __name__ == "__main__":

    fig = plt.figure(1)
    plt.ion()
    plt.show()
    print("Ploting...")

    balise = np.array([[-40, 40, 40, -40], [-40, -40, 40, 40]])
    beacon = [np.array([[0], [0]])+balise, np.array([[2000], [0   ]])+balise, np.array([[2000], [3000]])+balise, np.array([[0   ], [3000]])+balise]

    var = ''
    while var != 'quit':
        var = input("Please enter state: ")
        if var == 'quit':
            break
        var = var.split(',')
        x = int(var[0])
        y = int(var[1])
        o = int(var[2])
        data = getHokuyoData([x, y], o/180.0*np.pi, [np.array([[0, 2000, 2000, 0],[0, 0, 3000, 3000]])], 0)
        print(data)
        R = polar2cartesian(data)


        plt.clf()
        plt.axis([-3000, 3000, -3000, 3000])
        plt.scatter(R[0], R[1])
        #plt.scatter(data[0], data[1])
        plt.scatter([0], [0], c='red')
        plt.draw()
