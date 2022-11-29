import math
import numpy


EPSILON = 1e-09

class MyTuple:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def is_point(self):
        return math.isclose(self.w, 1)
    
    def is_vector(self):
        return math.isclose(self.w, 0)

    # if self.is_point():        #non funzia
    #     self.__class__ = Point
    # elif self.is_vector():
    #     self.__class__ = Vector

    def to_vector(self):
        if self.is_vector():
            return Vector(self.x, self.y, self.z)
    
    def __repr__(self):
        return f"MyTuple({self.x}, {self.y}, {self.z}, {self.w})"

    def round(self): #occhio non ho arrotondato w
        return create_tuple(round(self.x, ndigits=5), round(self.y, 5), round(self.z, 5), self.w)
    
    def __eq__(self, other):
        return math.isclose(self.x,other.x,
                            abs_tol=1e-14) and math.isclose(self.y,
                            other.y, abs_tol=1e-14) and math.isclose(self.z,
                            other.z, abs_tol=1e-14) and math.isclose(self.w, other.w,
                                                                         abs_tol=1e-14)
    
    def __add__(self, other):
        return create_tuple(self.x+ other.x, self.y + other.y,
                       self.z+ other.z, self.w + other.w)
    def __sub__(self, other):
        return create_tuple(self.x- other.x, self.y - other.y,
                       self.z- other.z, self.w - other.w)
    def __neg__(self):
        return create_tuple(0,0,0,0) -self
    
    def __mul__(self, c):
        return create_tuple(self.x *c, self.y*c, self.z*c, self.w*c)
    __rmul__= __mul__

    def __truediv__(self, scalar):
        return create_tuple(self.x/scalar, self.y/scalar, self.z/scalar,
                       self.w/scalar)
    def __floordiv__(self, scalar):
        return create_tuple(self.x/scalar, self.y/scalar, self.z/scalar,
                       self.w/scalar)

    # def dot(self, other):
    #     return self.x *other.x + self.y *other.y +self.z *other.z + self.w *other.w
    

    
    
class Point(MyTuple):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z 
        self.w = 1
    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"


class Vector(MyTuple):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z 
        self.w = 0
        
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    def magnitude(self):
        return math.sqrt(self.x**2 +self.y **2 +self.z **2)

    def normalize(self):
        m= self.magnitude()
        return Vector(self.x /m, self.y /m, self.z /m)

    def cross(self, b):
        return Vector(self.y*b.z - self.z*b.y,
                      self.z*b.x - self.x*b.z,
                      self.x*b.y - self.y*b.x)

    def reflect(self, normal):
        return self - 2*normal*self.dot(normal)



def create_tuple(x, y, z, w):
    if w==0:
        return Vector(x,y,z)
    elif w==1:
        return Point(x,y,z)
    else:
        return MyTuple(x,y,z,w)



    
class Projectile:
    def __init__(self, position: Point, velocity: Vector):

        self.position= position
        self.velocity= velocity
        
    def __repr__(self):
        return f"Projectile({self.position}, {self.velocity})"

class Environment:
    def __init__(self, gravity: Vector, wind: Vector):
        self.gravity= gravity
        self.wind = wind

    def __repr__(self):
        return f"Environment({self.gravity}, {self.wind})"
                                                      
    
def tick(env: Environment, proj: Projectile):
    """returns projectile with a new position and
    velocity after one unit of time"""

    pos = proj.position + proj.velocity
    vel = proj.velocity + env.gravity + env.wind
    return Projectile(pos, vel)

def trajectory(g, wind, x0, v0):
    """run tick(projectile) until y=0 ie it hits the ground 
    and count the number of ticks required"""

    e = Environment(g, wind)
    p = Projectile(x0, v0)
    traj = []
    while p.position.y >0 :
        traj.append(p)
        p= tick(e, p)
    return traj





















#class Matrix:
    #numpy.zeros((n,m))
    #numpy.identity(n)
    
def translation(x,y,z):
        return numpy.array([[1,0,0,x],
                       [0,1,0,y],
                       [0,0,1,z],
                       [0,0,0,1]])
def scaling(x,y,z):
        return numpy.array([[x,0,0,0],[0,y,0,0],[0,0,z,0],[0,0,0,1]])
    
def xrotation(r):
        return numpy.array([[1, 0, 0, 0],
                            [0,math.cos(r),-math.sin(r),0],
                            [0,math.sin(r), math.cos(r),0],
                            [0, 0, 0, 1]])
def yrotation(r):
        return numpy.array([[ math.cos(r),0,math.sin(r),0],
                       [0,1,0,0],
                       [-math.sin(r),0,math.cos(r),0],
                       [0, 0, 0, 1]])
def zrotation(r):
        return numpy.array([[math.cos(r),-math.sin(r),0,0],
                       [math.sin(r), math.cos(r),0,0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
def shear(x2,x3,y1,y3,z1,z2):
        return numpy.array([[1, x2,x3,0],
                       [y1,1, y3,0],
                       [z1,z2, 1,0],
                       [0, 0, 0, 1]])

def viewtransform(from0, to, up):
        forward = Vector.normalize(to-from0)
        upnormal = up.normalize()
        left = Vector.cross(forward,upnormal)
        trueup= Vector.cross(left, forward)

        orientation = numpy.array([[left.x, left.y, left.z, 0],
                                   [trueup.x, trueup.y, trueup.z, 0],
                                   [-forward.x, -forward.y, -forward.z, 0],
                                   [0,  0,  0,  1]])
        return orientation * translation(-from0.x, -from0.y, -from0.z)
    

    # np.array_equal(arr, arr1)
    # print((arr == arr1).all())
    # arr2 = np.allclose(arr, arr1)
    # np.array_equiv(arr, arr1)

def round5(matrix):
        return numpy.array([[ round(matrix[i,j],ndigits=5)  for j in range(matrix.shape[0]) ]
                                                            for i in range(matrix.shape[0]) ])


def dot(first, other: MyTuple):
    
        if first.__class__ == numpy.ndarray:   # (solo matrici 4x4)
            a = []        
            for i in range(4):
                a.append( first[i,0]*other.x + first[i,1]*other.y + first[i,2]*other.z + first[i,3]*other.w)
            return create_tuple(a[0], a[1], a[2], a[3])

        if first.__class__ in (MyTuple, Point,Vector):
            
            return first.x *other.x + first.y *other.y + first.z *other.z + first.w *other.w



    # def transpose(matrix):
    #     return numpy.array([[self[i,j] for i in range(self.mrows)]
    #                               for j in range(self.ncolumns)])
    
    # def submatrix(self, i0,j0):
    #     return Matrix([[self[i,j] for j in range(self.ncolumns) if j!=j0]
    #                                  for i in range(self.mrows) if i!=i0])

    # def minor(self, i0, j0):
    #     return Matrix.det(self.submatrix(i0,j0))

    # def cofactor(self, i,j):
    #     return (-1)**(i+j) * self.minor(i,j)

    # numpy.linalg.det(numpy.asarray(self.__data))

    # def invertible(self):
    #     return not(math.isclose(self.det(),0))

    # def inverse(self):
    #     assert(self.invertible()==True)
    #     inv = Matrix([[ self.cofactor(i,j)/ self.det()  for j in range(self.ncolumns)]
    #                                                      for i in range(self.mrows) ])
    #     inv = inv.transpose()
    #     return inv





    
    
# B = numpy.array([[-2,1,2,3.6567770989709897], [3,2,1,-1], [0,0,0,0], [6,7,8,9]])
# print(B)
# C =numpy.identity(4)
# #print( C)
# print(B @ numpy.identity(4))
# # print(round5(B))
# m = dot(B, MyTuple(1,2,3,4))
# print(m)
# #a = self[0,0]*other.x + self[0,1]*other.y + self[0,2]*other.z + self[0,3]*other.w
