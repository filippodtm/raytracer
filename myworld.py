import math
import mytuple  # for ray, sphere, lighting
import mycolor  # Material, light



#LIGHTING #############################################
class pointlight:
    def __init__(self, pos: mytuple.Point, intens: mycolor.Color):
        self.position= pos
        self.intensity = intens

    def equal(self, other):
        return self.position==other.position and self.intensity==other.intensity

class Material:
    def __init__(self,color= mycolor.Color(1,1,1), ambient=.1, diffuse=.9, specular=.9, shininess=200):
        self.color= color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

    def equal(self, other):
        return self.color==other.color and math.isclose(self.ambient,
                        other.ambient) and math.isclose(self.diffuse,
                        other.diffuse) and math.isclose(self.specular,
                       other.specular) and math.isclose(self.shininess,other.shininess)
    
    
def lighting(material: Material,
                    l: pointlight,
                point: mytuple.Point,
                  eye: mytuple.Vector,
               normal: mytuple.Vector):  
    sourcev = mytuple.Vector.normalize(l.position - point)
    ambient = l.intensity * material.color * material.ambient

    sourcedotnormal = sourcev.dot(normal)
    if sourcedotnormal < 0:
        #light source is on the other side
        diffuse = mycolor.Color.black()
        specular = mycolor.Color.black()
    else:
        diffuse = l.intensity * material.color *material.diffuse *  sourcedotnormal

        reflected = -sourcev.reflect(normal)
        if reflected.dot(eye) <=0:
            specular = mycolor.Color.black()
        else:
            k = reflected.dot(eye)**material.shininess
            specular = l.intensity * material.specular * k
    return ambient + diffuse + specular





#SPHERE, RAY, INTERSECTIONS

class sphere:
    def __init__(self):
        self.transform = mytuple.Matrix.Id()
        self.material  = Material()
    def settransform(self, m: mytuple.Matrix):
        self.transform = m
        
    def normal(self, p: mytuple.Point):
        p_wrtobj = self.transform.inverse() * p
        n_wrtobj = p_wrtobj - mytuple.Point(0,0,0)
        n = self.transform.inverse().transpose() * n_wrtobj

        n.w = 0   #serve se ho traslazioni
        return mytuple.Vector.normalize(n.to_vector())
    
    def equal(self,other):
        return self.transform.equal(other.transform) and self.material.equal(other.material)
    

class ray:
    def __init__(self, origin: mytuple.Point, direction: mytuple.Vector):
        self.origin= origin
        self.direction = direction
        
    def __repr__(self):
        return f"Ray({self.origin}, {self.direction}) "

    def position(self, t):
        return self.origin+ t* self.direction

    def inters(self, s: sphere):
        """compute ray-sphere intersections, with possible transformations"""
        ray2 = self.transform(s.transform.inverse())
        # vector center of sphere --> ray.origin
        v = ray2.origin - mytuple.Point(0,0,0)
        
        # look for t sol. of: ||v + t*dir||^2 = 1
        # ie:      |dir|^ t^ + 2<dir,v> t + |v|^ = 1
        a = mytuple.MyTuple.dot(ray2.direction,ray2.direction)
        b = 2* mytuple.MyTuple.dot(ray2.direction, v)
        c = mytuple.MyTuple.dot(v,v) -1
        delta = b**2 -4*a*c
        if delta<0:
            return ()
        else:
            t1 = (-b-math.sqrt(delta)) /(2*a)
            t2 = (-b+math.sqrt(delta)) /(2*a)
            return intersections(intersection(t1, s), intersection(t2,s))

    def transform(self, matr: mytuple.Matrix):
        o = matr* self.origin
        d = matr* self.direction
        return ray(o,d)



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
             'normal':i.obj.normal( r.position(i.t)) }

    if comps['normal'].dot(comps['eyev']) < 0: #inside
        comps['inside'] =True
        comps['normal'] =-comps['normal']
    return comps



# WORLD/SCENE #####################################################################

class Camera:

    def __init__(self, hsize:int, vsize:int, field:float):
        self.hsize = hsize
        self.vsize = vsize
        self.field = field
        self.transform = mytuple.Matrix.Id()

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

        pixel = self.transform.inverse() * mytuple.Point(worldx, worldy, -1)
        origin = self.transform.inverse() * mytuple.Point(0,0,0)

        return ray(origin, mytuple.Vector.normalize(pixel-origin))

    def render(self, w) -> mycolor.Canvas:
        
        image = mycolor.Canvas(self.hsize, self.vsize)

        for j in range(self.vsize):
            for i in range(self.hsize):
                r = self.rayforpixel(i,j)
                color = w.colorat(r)
                image.writepixel(i,j,color)
        return image




    
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
        s2.transform = mytuple.Matrix.scaling(.5, .5, .5)

        w = World()
        w.obj = [s1, s2]
        w.lightsource = l
        return w

    def intersectworld(self, r: ray): #(bastava hit?) #mi ordina le intersezioni di un ray coi vari objects
        res = []
        for elem in self.obj:
            res.extend( r.inters(elem))  # lista di intersections
        return sorted(res, key= lambda x: x.t)

    def shade_hit(self, comps: dict): # aus(solo per multiple lights)#
                                     #-> color at the intersection given by comps
        return lighting(comps['obj'].material, self.lightsource,
                        comps['point'], comps['eyev'], comps['normal'])

    def colorat(self, r: ray):   #finale
        intersezioni = self.intersectworld(r)
        h = hit(intersezioni)
        if not h:
            return mycolor.Color.black()
        else:
            comps = precomp(h, r)
            return self.shade_hit(comps)

        
