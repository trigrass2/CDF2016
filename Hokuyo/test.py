from MappingSLAM import Map
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

map = Map()

map.start()

'''
for i in range(200):
    print(map.bot_pos[-1])#, end='\r')
    #print(map.bot_pos[-1][0]-5000, map.bot_pos[-1][1]-5000, end='\r')
'''

sleep(50)

print(map.i)
mapbytes = bytearray(1000*1000)
map.slam.getmap(mapbytes)
w, h = 1000, 1000
data = np.zeros((h, w, 3), dtype=np.uint8)
for i in range(0,1000):
    for j in range(0,1000):
        data[i, j] = [mapbytes[i*1000+j], mapbytes[i*1000+j], mapbytes[i*1000+j]]


img = Image.fromarray(data, 'RGB')
img.save('my.png')
print("done")


sleep(5)

X = [2000-pos[0] for pos in map.bot_pos]
Y = [pos[1] for pos in map.bot_pos]

plt.figure(0, dpi=200)
plt.axis([0, 3000, 0, 2000])
plt.imshow(img, zorder=0, extent=[-2200, 4800, -2000, 5000])
plt.plot(Y, X,'b')
plt.show()

map.stop()