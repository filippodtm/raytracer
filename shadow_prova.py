import math
from mytuple import *
from mycolor import *


rayorigin= Point(0,0,-5)
wallz = 10
wallsize= 7
npixels= 100
# nomeppm?

def castshadow(rayorigin, wallz, wallsize, npixels, color=Color(1,0,0), shape=sphere()):
    """cast a shadow of the shape on a canvas"""

    pixelsize= wallsize/npixels #size of one pixel
    canvas = Canvas(npixels, npixels)
    half = wallsize/2
    for j in range(npixels):
        y = half - pixelsize*j # top: y=half, bottom: y=-half

        for i in range(npixels):
            x= -half + pixelsize*i #left x=-half, right x=half
            target = Point(x, y, wallz)
            r= ray(rayorigin, Vector.normalize(target-rayorigin)) #one ray to every pixel

            a = r.inters(shape)
            if hit(a):
                canvas.writepixel(i,j, color)
    
