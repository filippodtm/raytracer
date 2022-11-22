import math
from math import pi
from mytuple import *
from mycolor import *
from myworld import *


w = World()

floor = sphere()
floor.transform = Matrix.scaling(10, .01, 10)
floor.material.color = Color(1, .9, 9)
floor.material.specular = 0

leftwall = sphere()
leftwall.transform = Matrix.translation(0,0,5) * Matrix.yrotation(-pi
                                        /4) *Matrix.xrotation(pi/2) * Matrix.scaling(10, .01, 10)
leftwall.material = floor.material

rightwall = sphere()
rightwall.transform = Matrix.translation(0,0,5) * Matrix.yrotation(pi
                                        /4) *Matrix.xrotation(pi/2) * Matrix.scaling(10, .01, 10)

middle = sphere()
middle.transform = Matrix.translation(-0.5, 1, 0.5)
middle.material.color = Color(0.1, 1, .5)
middle.material.diffuse = 0.7
middle.material.specular = 0.3

right = sphere()
right.transform = Matrix.translation(1.5, 0.5, -0.5) * Matrix.scaling(.5, .5, .5)
right.material.color = Color(.5, 1, .1)
right.material.diffuse = 0.7
right.material.specular = 0.3

left = sphere()
left.transform = Matrix.translation(-1.5, 0.33, -0.75) * Matrix.scaling(.33, .33, .33)
left.material.color = Color(1, 0.8, .1)
left.material.diffuse = 0.7
left.material.specular = 0.3


w.obj = [floor, leftwall, rightwall, middle,right,left]
w.lightsource = pointlight(Point(-10, 10, -10), Color(1,1,1))
camera = Camera(100, 50, pi/3)
camera.transform = Matrix.viewtransform(Point(0, 1.5, -5), Point(0,1,0), Vector(0,1,0))

canvas = camera.render(w)
canvastoppm(canvas, 'scene1.ppm')