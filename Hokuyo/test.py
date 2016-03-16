from MappingSLAM import Map
import matplotlib.pyplot as plt

map = Map()

map.start()

plt.figure(0, dpi=200)
plt.ion()

for i in range(50):
    print(i)
    plt.clf()
    plt.axis([-1000, 1000, -1000, 1000])

    X = [pos[0]-5000 for pos in map.bot_pos]
    Y = [pos[1]-5000 for pos in map.bot_pos]

    print(map.bot_pos[-1])

    plt.plot(X, Y)
    plt.draw()


map.stop()