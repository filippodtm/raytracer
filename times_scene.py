# from scene_prova import *
from datetime    import datetime, timedelta
import matplotlib.pyplot as plt



valori = [ 5,10,20,50,100,200 ,300, 700, 1000 ]
tempi = []

# for n in valori:
#     tempi.append( scene_prova(n).total_seconds())


t = datetime.strptime("0:00:00.087167","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:00:00.474101","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:00:01.843536","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:00:09.123374","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:00:36.393461","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:02:52.441515","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:05:57.387858","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:34:43.950354","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

t = datetime.strptime("0:57:04.516518","%H:%M:%S.%f")
delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
tempi.append(delta)

 


print(valori, tempi)

plt.plot(valori, tempi)
plt.show()
