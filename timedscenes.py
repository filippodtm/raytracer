import scene1, scene2
from datetime import datetime
import matplotlib.pyplot as plt



valori = [ 40,200, 480, 640, 800, 1024 ]
tempi = []

for n in valori:
    tempi.append( scene2.scene2(n))

print(tempi)
plt.plot(valori, tempi)
plt.show()
