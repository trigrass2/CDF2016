from MappingSLAM import Map
import matplotlib.pyplot as plt
from time import sleep

map = Map()

map.start()
'''
for i in range(200):
    print('{:4.0f}'.format(map.bot_ori[-1]), end='\r')
    #print(map.bot_pos[-1][0]-5000, map.bot_pos[-1][1]-5000, end='\r')
'''

sleep(10)

X = [pos[0] for pos in map.bot_pos]
Y = [pos[1] for pos in map.bot_pos]

plt.figure(0, dpi=200)
plt.axis([-1000, 1000, -1000, 1000])
plt.plot(X, Y,'*b')
plt.show()

map.stop()