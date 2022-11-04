import math
import mytuple  #per trajectory()

class Color:
    
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return f"Color(r:{self.red}, g:{self.green}, b:{self.blue})"

    def __eq__(self, other):
        return math.isclose(self.red, other.red) and math.isclose(self.green,
                                    other.green) and math.isclose(self.blue, other.blue)

    # adding, subtracting colors
    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green,
                       self.blue + other.blue)
    def __sub__(self, other):
        return Color(self.red - other.red, self.green - other.green,
                       self.blue - other.blue)
    def __neg__(self):
        return Color(0,0,0,0) -self
    

    # multiplying and dividing by scalars
    def __mul__(self, k):
        if k.__class__== Color:
            return Color(self.red *k.red, self.green *k.green, self.blue *k.blue)
        else:
            return Color(self.red *k, self.green * k, self.blue* k)
    __rmul__= __mul__
    def __truediv__(self, scalar):
        return Color(self.red /scalar, self.green /scalar, self.blue /scalar)
    def __floordiv__(self, scalar):
        return Color(self.red /scalar, self.green /scalar, self.blue /scalar)

    # multiplying colors
    def hadamardprod(self, other):
        return Color(self.red *other.red, self.green *other.green, self.blue *other.blue)

    



    
class Canvas():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.grid = [[Color(0,0,0)] *height  for _ in range(width)]

    def __getitem__(self, tupla):
        x,y = tupla
        return self.grid[x][y]

    def writepixel(self, x,y, col):
        self.grid[x][y] = col
        #non prende self i,j
        
# canvas1= Canvas(2, 5)
# print(canvas1.grid)
# print("\n", canvas1[1,4]) 


def canvastoppm(canvas: Canvas, filename: str):
    with open(filename, "w+") as ppmfile:
        ppmfile.write(f"P3\n{canvas.width} {canvas.height}\n255\n")

        for y in range(canvas.height):
            n=0
            for x in range(canvas.width):
                scaledcolor = 255 * canvas.grid[x][y]
                colstr =  [str(round( max(0, min(scaledcolor.red, 255)))),
                           str(round(max(0, min(scaledcolor.green, 255)))),
                           str(round( max(0, min(scaledcolor.blue, 255))))]
                for i in colstr:
                    if n +len(i)>=69:
                        ppmfile.write("\n")
                        n=0
                    n+=len(i)+1
                    ppmfile.write(i+" ")
                
            ppmfile.write("\n")
        

def drawtrajectory(g, wind, x0, v0, canvaswidth, canvasheight, filename):
    canvas = Canvas(canvaswidth, canvasheight)
    trajectory = mytuple.trajectory(g, wind, x0, v0)
    for elem in trajectory:  # elem is Projectile(position,velocity)
        xi = round(elem.position.x)
        yi = canvasheight- round(elem.position.y)
        canvas.writepixel( xi,yi, Color(1,1,0))

    canvastoppm(canvas, filename)
