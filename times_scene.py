from scene_prova import *
from datetime    import datetime
import matplotlib.pyplot as plt



valori = [ 5,10,20,50,100, 150,200, 250,300, 400, 500 ]
tempi = []

for n in valori:
    tempi.append( scene_prova(n).total_seconds())


plt.plot(valori, tempi)
plt.show()
