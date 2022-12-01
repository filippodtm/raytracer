import math
import mytuple  #per trajectory(), #ray sphere ecc


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
    def round5(self):
        return Color(round(self.red, 5), round(self.green, 5), round(self.blue, 5))
    
    # adding, subtracting
    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green,
                       self.blue + other.blue)
    def __sub__(self, other):
        return Color(self.red - other.red, self.green - other.green,
                       self.blue - other.blue)
    def __neg__(self):
        return Color(0,0,0) -self
    

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

    
def black():
    return Color(0,0,0)
def white():
    return Color(0,0,0)
    



    
class Canvas:
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
                    if n +len(i)>=69:  #no lines longer than 70
                        ppmfile.write("\n")
                        n=0
                    n+=len(i)+1
                    ppmfile.write(i+" ")
                
            ppmfile.write("\n")













# class sphere:
#     def __init__(self):
#         self.transform = mytuple.Matrix.Id()
#         self.material  = Material()
        
#     def settransform(self, m: mytuple.Matrix):
#         self.transform = m
#     def normal(self, p: mytuple.Point):
#         p_wrtobj = self.transform.inverse() * p
#         n_wrtobj = p_wrtobj - mytuple.Point(0,0,0)
#         n = self.transform.inverse().transpose() * n_wrtobj

#         n.w = 0   #serve se ho traslazioni
#         return mytuple.Vector.normalize(n.to_vector())
       


# class intersection:
#     def __init__(self, t, obj):
#         self.t = t
#         self.obj = obj

# def intersections(*names): #inutile?
#     return names

# def hit(intersezioni: tuple):
#     """returns the intersection with lowest non negative t, if it exists"""
#     lista = [x for x in intersezioni if x.t>0]
#     if lista:
#         lista.sort(key=lambda x: x.t)
#         return lista[0]


# class ray:
#     def __init__(self, origin: mytuple.Point, direction: mytuple.Vector):
#         self.origin= origin
#         self.direction = direction
        
#     def __repr__(self):
#         return f"Ray({self.origin}, {self.direction}) "

#     def position(self, t):
#         return self.origin+ t* self.direction

#     def inters(self, s: sphere):
#         """compute ray-sphere intersections, with possible transformations"""
#         ray2 = self.transform(s.transform.inverse())
#         # vector center of sphere --> ray.origin
#         v = ray2.origin - mytuple.Point(0,0,0)
        
#         # look for t sol. of: ||v + t*dir||^2 = 1
#         # ie:      |dir|^ t^ + 2<dir,v> t + |v|^ = 1
#         a = mytuple.MyTuple.dot(ray2.direction,ray2.direction)
#         b = 2* mytuple.MyTuple.dot(ray2.direction, v)
#         c = mytuple.MyTuple.dot(v,v) -1
#         delta = b**2 -4*a*c
#         if delta<0:
#             return ()
#         else:
#             t1 = (-b-math.sqrt(delta)) /(2*a)
#             t2 = (-b+math.sqrt(delta)) /(2*a)
#             return intersections(intersection(t1, s), intersection(t2,s))

#     def transform(self, matr: mytuple.Matrix):
#         o = matr* self.origin
#         d = matr* self.direction
#         return ray(o,d)



# #
# class pointlight:
#     def __init__(self, pos: mytuple.Point, intens: Color):
#         self.position= pos
#         self.intensity = intens

# class Material:
#     def __init__(self,color= Color(1,1,1), ambient=.1, diffuse=.9, specular=.9, shininess=200):
#         self.color= color
#         self.ambient = ambient
#         self.diffuse = diffuse
#         self.specular = specular
#         self.shininess = shininess

#     def equal(self, other):
#         return self.color==other.color and math.isclose(self.ambient,
#                         other.ambient) and math.isclose(self.diffuse,
#                         other.diffuse) and math.isclose(self.specular,
#                        other.specular) and math.isclose(self.shininess,other.shininess)       




# def lighting(material: Material,
#              l:        pointlight,
#              point:    mytuple.Point,
#              eye:      mytuple.Vector,
#              normal:   mytuple.Vector):
    
#     sourcev = mytuple.Vector.normalize(l.position - point)
#     ambient = l.intensity * material.color * material.ambient

#     sourcedotnormal = sourcev.dot(normal)
#     if sourcedotnormal < 0:
#         #light source is on the other side
#         diffuse = Color.black()
#         specular = Color.black()
#     else:
#         diffuse = l.intensity * material.color *material.diffuse *  sourcedotnormal

#         reflected = -sourcev.reflect(normal)
#         if reflected.dot(eye) <=0:
#             specular = Color.black()
#         else:
#             k = reflected.dot(eye)**material.shininess
#             specular = l.intensity * material.specular * k
#     return ambient + diffuse + specular
