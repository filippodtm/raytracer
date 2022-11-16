import math
from mytuple import *
from mycolor import *


rayorigin = Point(0,0,-5)  #= osservatore
zwall = 10
wallsize= 20
npixels = 100

def castshadow(rayorigin,zwall,wallsize,npixels, luce, shape, filename= 'shadow.ppm'):

    pixelsize= wallsize/npixels #size of one pixel
    canvas = Canvas(npixels, npixels)
    half = wallsize/2
    for j in range(npixels):
        y = half - pixelsize*j # top: y=half, bottom: y=-half

        for i in range(npixels):
            x= -half + pixelsize*i #left x=-half, right x=half

            target = Point(x, y, zwall)
            r= ray(rayorigin, Vector.normalize(target-rayorigin))
            #one ray to every pixel  [rayorigin-->target]
            
            intrszn = r.inters(shape)
            if hit(intrszn):
                p_hit = r.position(hit(intrszn).t) # point where the ray hits the obj
                obj = hit(intrszn).obj            # =shape  #inutile??
                normal = obj.normal(p_hit)

                eyev = -r.direction
                colore = lighting(obj.material, luce, p_hit, eyev, normal)
                
                canvas.writepixel(i,j, colore)

    canvastoppm(canvas, filename)



shape1 = sphere()
shape1.material = Material()
shape1.material.color = Color(1, .2, 1)
#shape1.transform = Matrix.zrotation(math.pi /4)* Matrix.scaling(1, 0.2, 1)  * Matrix.zrotation(math.pi /4)
#print(shape1.transform)

luce = pointlight(Point(-8,8,-10), Color(1,1,1))

castshadow(rayorigin,zwall,wallsize,npixels,  luce, shape1, filename= 'shadow.ppm')
