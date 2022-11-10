import math
from mytuple import *
from mycolor import *


x0 = Point(0,1,0)
v0 = Vector(1,1.8,0).normalize() * 11.25
g= Vector(0,-0.1,0)
wind = Vector(-0.02 ,0,0)

#drawtrajectory(g, wind, x0, v0, 900, 550, "traiettoria1.ppm")
drawclockwise(canvaswidth =700, canvasheight= 550, filename='orologio1.ppm')




def clock(radius=1):
    l = []
    twelve = radius* Point(0,0,1)
    rot = Matrix.yrotation(math.pi/6)
    for i in range(12):
        l.append(twelve)
        twelve = rot*twelve
    return l

def drawclockwise(canvaswidth, canvasheight, filename='orologio1.ppm'):
    canvas = Canvas(canvaswidth, canvasheight)
    orol = clock(2/5* canvasheight)

    for elem in orol:  # elem is point
        xi = round(canvaswidth/2 + elem.x)
        yi = round(canvasheight/2 - elem.z) #in canvas y=0 è in alto
        canvas.writepixel( xi,yi, Color(1,1,0))

    canvastoppm(canvas, filename)


