import math
from mytuple import *
from mycolor import *

#run tick(projectile) until y=0 ie it hits the ground
#and count the number of ticks required

x0 = Point(0,1,0)
v0 = Vector(1,1.8,0).normalize() * 11.25
g= Vector(0,-0.1,0)
wind = Vector(-0.02 ,0,0)
#print(trajectory(g, wind, x0, v0))

drawtrajectory(g, wind, x0, v0, 900, 550, "traiettoria1.ppm")
