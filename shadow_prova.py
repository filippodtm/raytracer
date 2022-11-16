import math
from mytuple import *
from mycolor import *


rayorigin= Point(0,0,-5)
zwall = 10
wallsize= 20
npixels= 100

def castshadow(rayorigin, zwall, wallsize, npixels, shape, color=Color(1,0,0), filename= 'shadow.ppm'):
    """cast a shadow of the shape on a canvas"""

    pixelsize= wallsize/npixels #size of one pixel
    canvas = Canvas(npixels, npixels)
    half = wallsize/2
    for j in range(npixels):
        y = half - pixelsize*j # top: y=half, bottom: y=-half

        for i in range(npixels):
            x= -half + pixelsize*i #left x=-half, right x=half

            target = Point(x, y, zwall)
            r= ray(rayorigin, Vector.normalize(target-rayorigin)) #one ray to every pixel
            
            a = r.inters(shape)
            if hit(a):
                canvas.writepixel(i,j, color)
    canvastoppm(canvas, filename)



shape = sphere()

shape.transform = Matrix.zrotation(math.pi /4)* Matrix.scaling(1, 0.2, 1)  * Matrix.zrotation(math.pi /4)
print(shape, shape.transform)
castshadow(rayorigin, zwall, wallsize, npixels, shape, Color(1,0,0), filename= 'shadow.ppm')
