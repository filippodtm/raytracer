import scene1
from datetime import datetime
import matplotlib.pyplot as plt



valori = [ 40,200, 480, 640, 800, 1024, 1600 ]
tempi = []

for n in valori:
    tempi.append( scene1.scene1(n))

print(tempi)
plt.plot(valori, tempi)
plt.show()
