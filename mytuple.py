import math

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
        
    def __repr__(self):
        return f"MyTuple({self.x}, {self.y}, {self.z}, {self.w})"

    def __eq__(self, other):
        return math.isclose(self.x,other.x,
                            abs_tol=1e-14) and math.isclose(self.y,
                            other.y, abs_tol=1e-14) and math.isclose(self.z,
                            other.z, abs_tol=1e-14) and math.isclose(self.w, other.w,
                                                                         abs_tol=1e-14)
    
    def __add__(self, other):
        return MyTuple(self.x+ other.x, self.y + other.y,
                       self.z+ other.z, self.w + other.w)
    def __sub__(self, other):
        return MyTuple(self.x- other.x, self.y - other.y,
                       self.z- other.z, self.w - other.w)
    def __neg__(self):
        return MyTuple(0,0,0,0) -self

    
    def __mul__(self, c):
        return MyTuple(self.x *c, self.y*c, self.z*c, self.w*c)
    __rmul__= __mul__

    def __truediv__(self, scalar):
        return MyTuple(self.x/scalar, self.y/scalar, self.z/scalar,
                       self.w/scalar)
    def __floordiv__(self, scalar):
        return MyTuple(self.x/scalar, self.y/scalar, self.z/scalar,
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
        return Matrix( [[0]*n for _ in range(m)] )

    def Id():
        return Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

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

    
    
    def __init__(self, grid):
        self.checkvalidity(grid) #ha self ma non dipende da self
        
        self.__data = grid
        self.mrows = len(self.__data)
        self.ncolumns = len(self.__data[0])

    @staticmethod
    def checkvalidity(grid):
        m = len(grid)
        n = len(grid)
        for i in range(m):
            assert(len(grid[i])==n)

    def __getitem__(self, tupla):
        i,j = tupla
        return self.__data[i][j]

    def __repr__(self):
        output= "Matrix: \n"
        for i in range(self.mrows):
            output += ('|'+ ' |'.join(map(lambda elem: f'{elem: 9.8g}',
                                                          self.__data[i])) + '|\n')
        return output

    def __setitem__(self, tupla, value):
        i,j = tupla
        self.__data[i][j] = value
    
    def equal(self,other):
        res = True
        for i in range(self.mrows):
            for j in range(self.ncolumns):
                res &= math.isclose(self.__data[i][j], other.__data[i][j])
        return res
    
    def round(self):
        return Matrix([[ round(self[i,j],ndigits=5)  for j in range(self.ncolumns)]
                                                     for i in range(self.mrows)])

    
    def __mul__(self, other): #solo matrici 4x4
        if other.__class__==Matrix:
            return Matrix([[ sum([self[i,_]*other[_,j] for _ in range(self.ncolumns)])
                             #prodotto righe per colonne
                             for j in range(other.ncolumns)]
                              for i in range(self.mrows) ])
        
        elif other.__class__ in (MyTuple, Point,Vector):
            x,y,z,w = self[0,:]
            a = MyTuple.dot(MyTuple(x,y,z,w), other)
            x,y,z,w = self[1,:]
            b = MyTuple.dot(MyTuple(x,y,z,w), other)
            x,y,z,w = self[2,:]
            c = MyTuple.dot(MyTuple(x,y,z,w), other)
            x,y,z,w = self[3,:]
            d = MyTuple.dot(MyTuple(x,y,z,w), other)
            
            return MyTuple(a,b,c,d)

    def transpose(self):
        return Matrix([[self[i,j] for i in range(self.mrows)]
                                  for j in range(self.ncolumns)])
    
    def submatrix(self, i0,j0):
        return Matrix([[self[i,j] for j in range(self.ncolumns) if j!=j0]
                                     for i in range(self.mrows) if i!=i0])

    def minor(self, i0, j0):
        return Matrix.det(self.submatrix(i0,j0))

    def cofactor(self, i,j):
        return (-1)**(i+j) * self.minor(i,j)

    
    def det(self):
        assert(self.mrows == self.ncolumns)
        if self.mrows ==1:
                return self[0,0]
        elif self.mrows ==2:
                return self[0,0]*self[1,1] - self[1,0]*self[0,1]
        else:
            det=0
            #print(self.__data)
            for j in range(self.ncolumns):
                det += self[0,j]* self.cofactor(0,j)
        return det

    def invertible(self):
        return not(math.isclose(self.det(),0))

    def inverse(self):
        assert(self.invertible()==True)
        inv = Matrix([[ self.cofactor(i,j)/ self.det()  for j in range(self.ncolumns)]
                                                         for i in range(self.mrows) ])
        inv = inv.transpose()
        return inv



    
# B = Matrix([[-2,1,2,3], [3,2,1,-1]])
# print(B.transpose())
# print(B[1,0])
#a = self[0,0]*other.x + self[0,1]*other.y + self[0,2]*other.z + self[0,3]*other.w


















class sphere:
    def __init__(self):
        pass
    

s = sphere()
print(s)
    



class ray:
    def __init__(self, origin: Point, direction: Vector):
        self.origin= origin
        self.direction = direction
        
    def __repr__(self):
        return f"Ray({self.origin}, {self.direction}) "

    def position(self, t):
        return self.origin+ t* self.direction

    def intersect(self, s: sphere):
        #vector center of sphere --> ray.origin
        v = ray.origin - Point(0,0,0)

        # we look for t sol. of: ||v + t*dir||^2 =1
        # ie:      |dir|^ t^ + 2<dir,v> t + |v|^ = 1
        a = MyTuple.dot(ray.direction,ray.direction)
        b = 2* MyTuple.dot(ray.direction, v)
        c = MyTuple.dot(v,v) -1
        delta = b**2 -4*a*c
        if delta<0:
            return ()
        else:
            t1 = (-b-math.sqrt(delta)) /(2*a)
            t2 = (-b+math.sqrt(delta)) /(2*a)
            return (t1,t2)
        
