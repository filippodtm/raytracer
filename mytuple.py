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

    def dot(self, other):
        return self.x *other.x + self.y *other.y +self.z *other.z + self.w *other.w
    

    
    
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












class Matrix:
    @staticmethod
    def createzeros(m,n):
        return Matrix(numpy.zeros((m,n)))

    def Id():
        return Matrix(numpy.identity(4))
    
    @staticmethod
    def translation(x,y,z):
        return Matrix([[1,0,0,x],
                       [0,1,0,y],
                       [0,0,1,z],
                       [0,0,0,1]])
    @staticmethod
    def scaling(x,y,z):
        return Matrix([[x,0,0,0],[0,y,0,0],[0,0,z,0],[0,0,0,1]])
    
    @staticmethod
    def xrotation(r):
        return Matrix([[1, 0, 0, 0],
                       [0,math.cos(r),-math.sin(r),0],
                       [0,math.sin(r), math.cos(r),0],
                       [0, 0, 0, 1]])
    @staticmethod
    def yrotation(r):
        return Matrix([[ math.cos(r),0,math.sin(r),0],
                       [0,1,0,0],
                       [-math.sin(r),0,math.cos(r),0],
                       [0, 0, 0, 1]])
    @staticmethod
    def zrotation(r):
        return Matrix([[math.cos(r),-math.sin(r),0,0],
                       [math.sin(r), math.cos(r),0,0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    @staticmethod
    def shear(x2,x3,y1,y3,z1,z2):
        return Matrix([[1, x2,x3,0],
                       [y1,1, y3,0],
                       [z1,z2, 1,0],
                       [0, 0, 0, 1]])

    @staticmethod
    def viewtransform(from0, to, up):
        forward = Vector.normalize(to-from0)
        upnormal = up.normalize()
        left = Vector.cross(forward,upnormal)
        trueup= Vector.cross(left, forward)

        orientation = Matrix([[left.x, left.y, left.z, 0],
                              [trueup.x, trueup.y, trueup.z, 0],
                              [-forward.x, -forward.y, -forward.z, 0],
                              [0,  0,  0,  1]])
        return orientation * Matrix.translation(-from0.x, -from0.y, -from0.z)
    
    
    def __init__(self, grid):
        self.checkvalidity(grid) #ha self ma non dipende da self
        
        self.__data = numpy.array(grid)
        self.mrows = len(self.__data)
        self.ncolumns = len(self.__data[0])

    @staticmethod
    def checkvalidity(grid):
        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            assert(len(grid[i])==n)

            
    def __getitem__(self, tupla):
        # i,j = tupla
        return self.__data[tupla]

    def __repr__(self):
        return "Matrix: \n" + numpy.array_str(self.__data) #oppure array_repr()

    def __setitem__(self, tupla, value):
        i,j = tupla
        self.__data[i,j] = value
    
    def equal(self,other):
        return numpy.array([[math.isclose(self[i,j], other[i,j])  for j in range(self.ncolumns)]
                                                                  for i in range(self.mrows)]).all()

    def round(self):
        return Matrix([[ round(self[i,j],ndigits=5)  for j in range(self.ncolumns)]
                                                     for i in range(self.mrows)])

    def __mul__(self, other): #solo matrici 4x4
        if other.__class__==Matrix:
            return Matrix( self.__data @ other.__data)
        
        elif other.__class__ in (MyTuple, Point,Vector):  #intanto
            a = []
            for i in range(4):
                a.append( self[i,0]*other.x + self[i,1]*other.y + self[i,2]*other.z + self[i,3]*other.w)
            return create_tuple(a[0], a[1], a[2], a[3])

    def transpose(self):
        return Matrix(self.__data.transpose())
    
    def submatrix(self, i0,j0):
        return Matrix([[self.__data[i,j] for j in range(self.ncolumns) if j!=j0]
                                       for i in range(self.mrows) if i!=i0])

    def minor(self, i0, j0):
        return Matrix.det(self.submatrix(i0,j0))

    def cofactor(self, i,j):
        return (-1)**(i+j) * self.minor(i,j)
    
    def det(self):
            return numpy.linalg.det(self.__data)

    def invertible(self):
        assert(self.mrows == self.ncolumns)
        return not(math.isclose(self.det(),0))

    def inverse(self):
        inv = numpy.linalg.inv(self.__data)
        return Matrix(inv)





# A = Matrix([[1,0], [0,1]])
# B = Matrix([[0,1,2,3],
#             [1,0,5,0],
#             [2,5,0,6],
#             [3,0,6,0]])
# print(Matrix.equal(A, A.transpose() ))
# #B[1,1] = 23234
# # C = A*B
# print(B[1,1])
# print(B.submatrix(0,2))

