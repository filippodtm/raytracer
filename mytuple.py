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
    
    def __repr__(self):
        return f"MyTuple({self.x}, {self.y}, {self.z}, {self.w})"

    def __eq__(self, other):
        return math.isclose(self.x, other.x) and math.isclose(self.y,
                                    other.y) and math.isclose(self.z,
                                    other.z) and math.isclose(self.w, other.w)

    
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

        #if position.is_point() and velocity.is_vector():
        #    position.__class__ = Point
        #    velocity.__class__ = Vector
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
    def createzeros(m,n):
        return Matrix( [[0]*n for _ in range(m)] )

    def Id():
        return Matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    
    def __init__(self, data):
        self.__data = data
        self.checkvalidity()
        self.mrows = len(data)
        self.ncolumns = len(data[0])

    def checkvalidity(self):
        m = len(self.__data)
        n = len(self.__data[0])
        for i in range(m):
            assert(len(self.__data[i])==n)

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

    
    def __mul__(self, other):
        if other.__class__==Matrix:
            return Matrix([[ sum([self[i,_]*other[_,j] for _ in range(self.ncolumns)])
                             #prodotto righe per colonne
                             for j in range(other.ncolumns)]
                              for i in range(self.mrows) ])
        
        elif other.__class__==MyTuple: #solo matrici 4x4
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


# m = Matrix([[2,0.009999],[3,4.000000000000000000]])

