import math
import mytuple  # ray, sphere, lighting
import mycolor  # Material, light



# Materials #############################################
class pointlight:
    def __init__(self, pos: mytuple.Point, intens: mycolor.Color):
        self.position = pos
        self.intensity = intens

    def equal(self, other):
        return self.position==other.position and self.intensity==other.intensity

class Material:
    def __init__(self,color= mycolor.Color(1,1,1), ambient=.1, diffuse=.9, specular=.9, shininess=200, pattern=None):
        self.color= color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.pattern = pattern

    def equal(self, other):
        return self.color==other.color and math.isclose(self.ambient,
                        other.ambient) and math.isclose(self.diffuse,
                        other.diffuse) and math.isclose(self.specular,
                       other.specular) and math.isclose(self.shininess,
                      other.shininess) # and self.pattern.equal(other.pattern)





def f0(a,b, point): return mycolor.Color(point.x, point.y, point.z)

class Pattern:
    def __init__(self, f=f0, colora=None, colorb=None, transf=mytuple.Matrix.Id()):
        self.func = f
        self.a = colora
        self.b = colorb
        self.transformation= transf
        
    def pattern_at(self, point):
        return self.func(self.a, self.b, point)

def stripe(a,b, point):
    if math.floor(point.x)%2==0:
        return a
    else: return b
def gradient(a,b,point):
    return a + (b-a)* (point.x- math.floor(point.x))
def rings(a,b,p):
    if math.floor( math.sqrt((p.x)**2 +(p.z)**2)) %2==0:
        return a
    else: return b
def checker(a,b, p):
    d= math.floor(p.x) +math.floor(p.y)+math.floor(p.z)
    if d %2==0:
        return a
    else: return b


    

# p= Pattern(stripe, mycolor.white(), mycolor.black())
# print(p.pattern_at(mytuple.Point(0,0,0)))



#SPHERE, RAY, INTERSECTIONS ##############################################################


class Shape:
    def __init__(self):
        self.transformation= mytuple.Matrix.Id()
        self.material = Material()
        # transform ray by inverse
        # for normal, convert point to objsp, then normal* inv^T
        
    def settransform(self, m: mytuple.Matrix):
        self.transformation= m

    def equal(self,other):
        return self.transformation.equal(other.transformation) and self.material.equal(other.material)

    def patternshape_at(self, point_wrtworld):
        point_wrtobj = self.transformation.inverse() * point_wrtworld
        ptrn = self.material.pattern
        point_wrtpattern= ptrn.transformation.inverse() * point_wrtobj
        return ptrn.pattern_at(point_wrtpattern)


    def normal_at(self, p: mytuple.Point):
        localpoint = self.transformation.inverse() * p

        localnormal = self.localnormal_at(localpoint)
        
        n_world = self.transformation.inverse().transpose() * localnormal
        n_world.w = 0   # se ho traslazioni
        return mytuple.Vector.normalize(n_world.to_vector())

    def localnormal_at(self, p):
        return mytuple.Vector(p.x, p.y, p.z) #inutile

    
    def localintersect(self, localray):
        self.savedray = localray
        # + localintersect di sphere/ecc



class sphere(Shape):
    def localnormal_at(self, localpoint):
        return localpoint - mytuple.Point(0,0,0)
        
    def localintersect(self, localray):
        """compute localray-sphere intersections"""
        super().localintersect(localray)
        
        # vector center of sphere --> ray.origin
        v = localray.origin - mytuple.Point(0,0,0)
        # look for t sol. of: ||v + t*dir||^2 = 1
        # ie:      |dir|^ t^ + 2<dir,v> t + |v|^ = 1
        a = mytuple.MyTuple.dot(localray.direction,localray.direction)
        b = 2* mytuple.MyTuple.dot(localray.direction, v)
        c = mytuple.MyTuple.dot(v,v) -1
        delta = b**2 -4*a*c
        if delta<0:
            return ()
        else:
            t1 = (-b-math.sqrt(delta)) /(2*a)
            t2 = (-b+math.sqrt(delta)) /(2*a)
            return intersections(intersection(t1, self), intersection(t2,self))

class Plane(Shape):
    def localnormal_at(self, p):
        return mytuple.Vector(0,1,0)

    def localintersect(self, localray):
        if abs(localray.direction.y) > mytuple.EPSILON:
            t = -localray.origin.y / localray.direction.y
            return [intersection(t,self)]
        #(se < EPS return none)


class ray:
    def __init__(self, origin: mytuple.Point, direction: mytuple.Vector):
        self.origin= origin
        self.direction = direction
        
    def __repr__(self):
        return f"Ray({self.origin}, {self.direction}) "

    def position(self, t):
        return self.origin+ t* self.direction

    def inters(self, s: sphere):
        localray = self.transform(s.transformation.inverse())   
        return s.localintersect(localray)


    def transform(self, matr: mytuple.Matrix):
        o = matr* self.origin
        d = matr* self.direction
        return ray(o,d)







def lighting(#material: Material,  #ometto
                 obj : Shape,
                   l : pointlight,
                point: mytuple.Point,
                  eye: mytuple.Vector,
               normal: mytuple.Vector,
             inshadow= False):

    if obj.material.pattern:   #pag130
        col = obj.patternshape_at( point)
    else:
        col = obj.material.color
    
    sourcev = mytuple.Vector.normalize(l.position - point)
    ambient = l.intensity * col * obj.material.ambient
    if inshadow:
        return ambient 
    
    sourcedotnormal = sourcev.dot(normal)
    if sourcedotnormal < 0:
        #light source is on the other side
        diffuse = mycolor.black()
        specular = mycolor.black()
    else:
        diffuse = l.intensity * col *obj.material.diffuse *  sourcedotnormal

        reflected = -sourcev.reflect(normal)
        if reflected.dot(eye) <=0:
            specular = mycolor.black()
        else:
            k = reflected.dot(eye)**obj.material.shininess
            specular = l.intensity * obj.material.specular * k
    return ambient + diffuse + specular








    

class intersection:
    def __init__(self, t, obj):
        self.t = t
        self.obj = obj

def intersections(*names): #inutile?
    return list(names)

def hit(intersezioni: list):
    #"""returns the one with lowest non negative t, if it exists"""
    lista = [x for x in intersezioni if x.t>0]
    if lista:
        lista.sort(key=lambda x: x.t)
        return lista[0]


def precomp( i: intersection, r: ray):  #returns info on that intersection

    comps = {'t':i.t,
             'obj':i.obj,
             'point':r.position(i.t),
             'eyev':-r.direction,
             'inside':False,
             'normal':i.obj.normal_at( r.position(i.t)) }

    if comps['normal'].dot(comps['eyev']) < 0: #inside
        comps['inside'] =True
        comps['normal'] =-comps['normal']

    comps['pointover'] = comps['point']+ mytuple.EPSILON *comps['normal']
    return comps








# WORLD/SCENE #####################################################################

class World:
    def __init__(self):
        self.obj = []
        self.lightsource = None

    @staticmethod
    def defaultworld():
        l = pointlight(mytuple.Point(-10,10,-10), mycolor.Color(1,1,1))
        s1 = sphere()
        s1.material.color = mycolor.Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular= 0.2
        s2 = sphere()
        s2.transformation= mytuple.Matrix.scaling(.5, .5, .5)

        w = World()
        w.obj = [s1, s2]
        w.lightsource = l
        return w

    def intersectworld(self, r: ray): #(bastava hit?)
        #mi ordina le intersezioni di un ray coi vari objects
        res = []
        for elem in self.obj:
            res.extend( r.inters(elem))  # lista di intersections
        return sorted(res, key= lambda x: x.t)

    def shade_hit(self, comps: dict):#(qui per multiple lights)#
        inshadow = self.isinshadow(comps['pointover']) #usa 'pointover'
        
        return lighting(#comps['obj'].material,
                        comps['obj'],
                        self.lightsource,
                        comps['pointover'],
                        comps['eyev'],
                        comps['normal'], inshadow)
                        # -> color at the intersection given by comps

    def colorat(self, r: ray):   #finale
        intersezioni = self.intersectworld(r)
        h = hit(intersezioni)
        if not h:
            return mycolor.black()
        else:
            comps = precomp(h, r)
            return self.shade_hit(comps)

        
    def isinshadow(self, point):
        #(chap8) send a ray from point to lightsource. if it hits smth, point is in shadow
        
        v = self.lightsource.position - point
        distance = v.magnitude()
        r = ray(point, v.normalize())
        intersz = self.intersectworld(r)

        h = hit(intersz)
        if h  and  h.t <distance:
            return True
        else:
            return False









class Camera:

    def __init__(self, hsize:int, vsize:int, field:float):
        self.hsize = hsize
        self.vsize = vsize
        self.field = field
        self.transformation = mytuple.Matrix.Id()

        #pixelsize:
        half_view= math.tan(self.field /2)
        aspect = self.hsize / self.vsize
        if aspect >=1:
            self.halfwidth  = half_view
            self.halfheight = half_view / aspect
        else:
            self.halfwidth  = half_view * aspect
            self.halfheight = half_view
            
        self.pixelsize = self.halfwidth*2 / self.hsize

    def rayforpixel(self, i,j):  #sdm
        xoffset = (i+.5)* self.pixelsize
        yoffset = (j+.5)* self.pixelsize
        worldx = self.halfwidth - xoffset
        worldy = self.halfheight -yoffset

        pixel = self.transformation.inverse() * mytuple.Point(worldx, worldy, -1)
        origin = self.transformation.inverse() * mytuple.Point(0,0,0)

        return ray(origin, mytuple.Vector.normalize(pixel-origin))

    def render(self, w) -> mycolor.Canvas:
        
        image = mycolor.Canvas(self.hsize, self.vsize)

        for j in range(self.vsize):
            for i in range(self.hsize):
                r = self.rayforpixel(i,j)
                color = w.colorat(r)
                image.writepixel(i,j,color)
        return image

