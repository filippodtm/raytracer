import math
from math import pi
from datetime import datetime
import sys

from mytuple import *
from mycolor import *
from myworld import *


w = World()

floor = Plane()
floor.material = Material()
floor.material.color = Color(1, .9, .9)
floor.material.specular = 0
floor.material.pattern = Stripepattern(white(), mycolor.Color(1,0,0))

# leftwall = sphere()
# leftwall.transformation = Matrix.translation(0,0,5) * Matrix.yrotation(-pi
#                     /4) *Matrix.xrotation(pi/2) * Matrix.scaling(10, .01, 10)
# leftwall.material = floor.material
# leftwall.material.color = Color(1, .9, .9)
# leftwall.material.specular = 0

backdrop = Plane()
backdrop.transformation = Matrix.translation(0,0,6)* Matrix.xrotation(pi/2)
backdrop.material.pattern = Stripepattern(white(), Color(1,0,0))


middle = sphere()
middle.material.pattern = Stripepattern(Color(1,0,0), white())
middle.transformation = Matrix.translation(-0.5, 1, .5) #* Matrix.shear(1,1, 0,1, 0,0)
#middle.material.color = Color(.1, 1, .5)
# middle.material.diffuse = 0.7
# middle.material.specular = 1 #

right = sphere()
right.transformation = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(.5, .5, .5)
right.material.color = Color(.5, 1, .1)
right.material.diffuse = 0.7
right.material.specular = 0.3

left = sphere()
left.transformation = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(.33, .33, .33)
left.material.color = Color(1, .4, .1) #
left.material.diffuse = 0.7
left.material.specular = 0.5 #


w.obj = [floor, backdrop, middle]
w.lightsource = pointlight(Point(-10, 10, -10), Color(1,1,1))



def scene2(n):
    start = datetime.now()
    
    camera = Camera(n, round(3/4*n), pi/3)
    camera.transformation = Matrix.viewtransform(Point(0, 1.5, -5), Point(0,1,0), Vector(0,1,0))
    canvas = camera.render(w)
    canvastoppm(canvas, 'scene_2.ppm')

    print(f"{ datetime.now()-start } (h:min:sec._)   ------>  risoluzione {n}x{int(3/4*n)}   ")
    return (datetime.now()-start).total_seconds()



################################################################################




# solo quando voglio eseguire questo file
if __name__ == '__main__':
    
    input1 = int(sys.argv[1])
    
    scene2(input1)
