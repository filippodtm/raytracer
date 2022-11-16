import unittest
import math

import mytuple
import mycolor

class TupleTest(unittest.TestCase):

    def test_ATupleIsAPointOrvector(self):
        a = mytuple.MyTuple(4.3, -4.2, 3.1, 1.0)

        self.assertEqual(4.3, a.x)
        self.assertEqual(-4.2, a.y)
        self.assertEqual(3.1, a.z)
        self.assertEqual(1.0, a.w)
        self.assertTrue(a.is_point())
        self.assertFalse(a.is_vector())

    def test_pointcreatesTuplewith1(self):
        a = mytuple.Point(4,-4,3)

        self.assertEqual(a, mytuple.MyTuple(4,-4,3,1))

    def test_vectorcreatesTuplewith0(self):
        a = mytuple.Vector(4,-4,3)

        self.assertEqual(a, mytuple.MyTuple(4,-4,3,0))

    def test_addingtuples(self):
        a1 = mytuple.MyTuple(3,-2,5,1)
        a2 = mytuple.MyTuple(-2,3,1,0)
        #somma point+point->non ha senso, w=2

        self.assertEqual(a1+a2, mytuple.MyTuple(1,1,6,1))

    
    def test_subtractingtuples(self):
        p1 = mytuple.Point(3,2,1)
        p2 = mytuple.Point(5,6,7)
        v1 = mytuple.Vector(3,2,1)
        v2 = mytuple.Vector(5,6,7)

        self.assertEqual(p1+(-p2), mytuple.Vector(-2,-4,-6))
        self.assertEqual(p1+(-v2), mytuple.Point(-2,-4,-6))
        self.assertEqual(v1-v2, mytuple.Vector(-2,-4,-6))
    
    def test_negatingtuples(self):
        a = mytuple.MyTuple(1, -2, 3, -4)

        self.assertEqual(-a, mytuple.MyTuple(-1,2,-3,4))

    def test_multbyscalar(self):
        a= mytuple.MyTuple(1,-2,3,-4)

        self.assertEqual(a*3.5, mytuple.MyTuple(3.5, -7, 10.5, -14))
        self.assertEqual(a*0.5, mytuple.MyTuple(0.5, -1, 1.5, -2))

    def test_dividebyscalar(self):
        a= mytuple.MyTuple(1,-2,3,-4)
        
        self.assertEqual(a/2 , mytuple.MyTuple(0.5, -1, 1.5, -2))

    def test_checkmagnitude(self):
        v1= mytuple.Vector(1,0,0)
        v2= mytuple.Vector(0,1,0)
        v3= mytuple.Vector(0,0,1)
        v4= mytuple.Vector(1,2,3)
        v5= mytuple.Vector(-1,-2,-3)

        self.assertEqual(mytuple.Vector.magnitude(v1), 1)
        self.assertEqual(mytuple.Vector.magnitude(v2), 1)
        self.assertEqual(mytuple.Vector.magnitude(v3), 1)
        self.assertEqual(mytuple.Vector.magnitude(v4), math.sqrt(14))
        self.assertEqual(mytuple.Vector.magnitude(v5), math.sqrt(14))
    
    def test_normalization(self):
        v1= mytuple.Vector(4,0,0)
        v2= mytuple.Vector(1,2,3)

        self.assertEqual(mytuple.Vector.normalize(v1), mytuple.Vector(1,0,0))
        self.assertEqual(mytuple.Vector.normalize(v2), mytuple.Vector(1/math.sqrt(14),
                                                    2/math.sqrt(14), 3/math.sqrt(14)))
        self.assertEqual(mytuple.Vector.magnitude(mytuple.Vector.normalize(v2)), 1)

    def test_dotcrossproduct(self):
        v1= mytuple.Vector(1,2,3)
        v2= mytuple.Vector(2,3,4)
        
        self.assertEqual(mytuple.MyTuple.dot(v1,v2), 20)

        self.assertEqual(mytuple.Vector.cross(v1,v2), mytuple.Vector(-1,2,-1))
        self.assertEqual(mytuple.Vector.cross(v2,v1), mytuple.Vector(1,-2,1))

    
    

class ColorTest(unittest.TestCase):
    def test_colorsaretuples(self):
        c = mycolor.Color(-0.5, 0.4, 1.7)

        self.assertEqual(c.red, -0.5)
        self.assertEqual(c.green, 0.4)
        self.assertEqual(c.blue, 1.7)

    def test_colorOperations(self):
        c1= mycolor.Color(0.9, 0.6, 0.75)
        c2= mycolor.Color(0.7, 0.1, 0.25)
        c= mycolor.Color(.2, .3, .4)
        
        self.assertEqual(c1+c2, mycolor.Color(1.6, 0.7, 1.0))
        self.assertEqual(c1-c2, mycolor.Color(0.2, 0.5, 0.5))
        self.assertEqual(c * 2, mycolor.Color(.4, .6, .8))

    def test_multiplycolors(self):
        c1 = mycolor.Color(1, .2, .4)
        c2 = mycolor.Color(.9, 1, .1)

        self.assertEqual(c1* c2, mycolor.Color(.9, .2, .04))
        self.assertEqual(mycolor.Color.hadamardprod(c1, c2), mycolor.Color(.9, .2, .04))



        

class CanvasTest(unittest.TestCase):
    
    def test_creatingcanvas(self):
        c = mycolor.Canvas(10, 20)

        self.assertEqual(c.width, 10)
        self.assertEqual(c.height, 20)
        for j in range(c.width):
            for i in range(c.height): 
                 self.assertEqual(c[j,i], mycolor.Color(0,0,0))

    def test_writingpixels(self):
        c = mycolor.Canvas(10, 20)
        red = mycolor.Color(1,0,0)
        mycolor.Canvas.writepixel(c,2,3,red)
        
        self.assertEqual(c[2,3] , red )


    def test_PPMheader(self):
        c= mycolor.Canvas(5,3)
        
        mycolor.canvastoppm(c, "ppmfile.ppm")
        with open("ppmfile.ppm" ,"r") as ppmfile:
            ppmlines= ppmfile.readlines()

        self.assertEqual(ppmlines[0], "P3\n")
        self.assertEqual(ppmlines[1], "5 3\n")
        self.assertEqual(ppmlines[2], "255\n")
        

    def test_PPMwritepixels(self):
        c = mycolor.Canvas(5,3)
        c1 = mycolor.Color(1.5, 0, 0)
        c2 = mycolor.Color(0, 0.5, 0)
        c3 = mycolor.Color(-0.5, 0, 1)
        mycolor.Canvas.writepixel(c,0,0, c1)
        mycolor.Canvas.writepixel(c,2,1, c2)
        mycolor.Canvas.writepixel(c,4,2, c3)

        mycolor.canvastoppm(c, "ppmfile.ppm")
        
        with open("ppmfile.ppm" ,"r") as ppmfile:
            ppmlines= ppmfile.readlines()

        self.assertEqual(ppmlines[3], "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \n")
        self.assertEqual(ppmlines[4], "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0 \n")
        self.assertEqual(ppmlines[5], "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255 \n")

    def test_longPPMlines(self):
        c = mycolor.Canvas(10,2)
        color1 = mycolor.Color(1, 0.8, 0.6)
       
        for y in range(c.height):
            for x in range(c.width):
                mycolor.Canvas.writepixel(c, x,y, color1)    #set all pixels of c with color1
                
        mycolor.canvastoppm(c, "ppm.ppm")
        
        with open("ppm.ppm" ,"r") as ppmfile:
            ppmlines= ppmfile.readlines()

        self.assertEqual(ppmlines[3], "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204 \n")
        self.assertEqual(ppmlines[4], "153 255 204 153 255 204 153 255 204 153 255 204 153 \n")
        self.assertEqual(ppmlines[5], "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204 \n")
        self.assertEqual(ppmlines[6], "153 255 204 153 255 204 153 255 204 153 255 204 153 \n")

    def test_PPMending(self):
        c = mycolor.Canvas(5,3)
        mycolor.canvastoppm(c, "ppm.ppm")

        with open("ppm.ppm" ,"r") as ppmfile:
            ppmlines= ppmfile.readlines()

        self.assertEqual(ppmlines[-1][-1], "\n")








        


class Matrixtest(unittest.TestCase):

    def test_creatematrix(self):
        M = mytuple.Matrix([[1,2,3,4],[5.5, 6.5, 7.5, 8.5],
                            [9,10,11,12],[13.5,14.5,15.5,16.5]])

        self.assertEqual(M[0,0], 1)
        self.assertEqual(M[0,3], 4)
        self.assertEqual(M[1,0], 5.5)
        self.assertEqual(M[1,2], 7.5)
        self.assertEqual(M[2,2], 11)
        self.assertEqual(M[3,0], 13.5)
        self.assertEqual(M[3,2], 15.5)
        

    def test_create2x2matrix(self):
        M = mytuple.Matrix([[-3,5],[1,-2]])

        self.assertEqual(M[0,0], -3)
        self.assertEqual(M[0,1], 5)
        self.assertEqual(M[1,0], 1)
        self.assertEqual(M[1,1], -2)

    def test_create3x3matrix(self):
        M = mytuple.Matrix([[-3,5, 0], [1,-2,-7],[0, 1, 1]])

        self.assertEqual(M[0,0], -3)
        self.assertEqual(M[1,1], -2)
        self.assertEqual(M[2,2], 1)

    def test_equalmatrix(self):
        A = mytuple.Matrix([[1,2,3,4],[5,6,7,8],[9,8,7,6],[5,4,3,2]])
        B = mytuple.Matrix([[1,2,3,4],[5,6,7,8],[9,8,7,6],[5,4,3,2]])

        self.assertEqual(A.equal(B), True)

    def test_notequalmatrix(self):
        A = mytuple.Matrix([[1,2,3,4],
                            [5,6,7,8],
                            [9,8,7,6],
                            [5,4,3,2]])
        B = mytuple.Matrix([[2,3,4,5],
                            [6,7,8,9],
                            [8,7,6,5],
                            [4,3,2,1]])

        self.assertEqual(A.equal(B), False)

    def test_matrixmult(self):
        A = mytuple.Matrix([[1,2,3,4],
                            [5,6,7,8],
                            [9,8,7,6],
                            [5,4,3,2]])
        B = mytuple.Matrix([[-2,1,2, 3],
                            [3, 2,1,-1],
                            [4, 3,6, 5],
                            [1, 2,7, 8]])
        C = mytuple.Matrix([[20,22, 50, 48],
                            [44,54,114,108],
                            [40,58,110,102],
                            [16,26, 46, 42]])
        self.assertEqual( C.equal(A*B), True)

    def test_matrixtuple(self):
        A = mytuple.Matrix([[1,2,3,4],
                            [2,4,4,2],
                            [8,6,4,1],
                            [0,0,0,1]])
        b = mytuple.MyTuple(1,2,3,1)
        c = mytuple.MyTuple(18,24,33,1)

        self.assertEqual(A*b, c)

    def test_matrixbyidentity(self):
        A = mytuple.Matrix([[0,1, 2, 4],
                            [1,2, 4, 8],
                            [2,4, 8,16],
                            [4,8,16,32]])

        self.assertEqual(A.equal(A* mytuple.Matrix.Id()), True)

    def test_tuplebyidentity(self):
        a = mytuple.MyTuple(1,2,3,4)

        self.assertEqual(mytuple.Matrix.Id() *a, a)

    def test_transpose(self):
        A = mytuple.Matrix([[0,9,3,0],
                            [9,8,0,8],
                            [1,8,5,3],
                            [0,0,5,8]])
        B = mytuple.Matrix([[0,9,1,0],
                            [9,8,8,0],
                            [3,0,5,5],
                            [0,8,3,8]])
        C = mytuple.Matrix.Id().transpose()
        self.assertEqual(A.transpose().equal(B), True)
        self.assertEqual(C.equal(mytuple.Matrix.Id()), True)

        
    def test_2x2determinant(self):
        A = mytuple.Matrix([[1,5],[-3,2]])

        self.assertEqual(A.det(), 17)
        
    def test_submatrix(self):
        A= mytuple.Matrix([[ 1,5,0],
                           [-3,2,7],
                           [ 0,6,-3]])
        self.assertEqual(A.submatrix(0,2).equal(mytuple.Matrix([[-3,2],
                                                                [0,6]])), True)
        B= mytuple.Matrix([[-6,1, 1,6],
                           [-8,5, 8,6],
                           [-1,0, 8,2],
                           [-7,1,-1,1]])
        self.assertEqual(B.submatrix(2,1).equal(mytuple.Matrix([[-6, 1,6],
                                                           [-8, 8,6],
                                                                [-7,-1,1]])), True)
    def test_minor_cofactor(self):
        A= mytuple.Matrix([[3, 5,0],
                           [2,-1,-7],
                           [6,-1,5]])
        B = A.submatrix(1,0)
        
        self.assertEqual(B.det(), 25)
        self.assertEqual(A.minor(1,0), 25)

        self.assertEqual(A.cofactor(1,0),-25)

        self.assertEqual(A.minor(0,0),  -12)
        self.assertEqual(A.cofactor(0,0),-12)
        
    def test_3x3determinant(self):
        A = mytuple.Matrix([[1, 2,6],
                            [-5,8,-4],
                            [2, 6, 4]])
        self.assertEqual(A.cofactor(0,0), 56)
        self.assertEqual(A.cofactor(0,1), 12)
        self.assertEqual(A.cofactor(0,2),-46)

        self.assertEqual(A.det(),-196)

    def test_4x4determinant(self):
        A = mytuple.Matrix([[-2,-8,3,5],
                            [-3, 1,7,3],
                            [1, 2,-9,6],
                            [-6,7,7,-9]])
        self.assertEqual(A.cofactor(0,0), 690)
        self.assertEqual(A.cofactor(0,1), 447)
        self.assertEqual(A.cofactor(0,2), 210)
        self.assertEqual(A.cofactor(0,3), 51)

        self.assertEqual(A.det(),-4071)

    def test_isinvertible(self):
        A = mytuple.Matrix([[6,4,4,4],
                            [5,5,7,6],
                            [4,-9,3,-7],
                            [9,1,7,-6]])
        self.assertEqual(A.det(),-2120)
        self.assertEqual(A.invertible(), True)
        
        B = mytuple.Matrix([[-4,2,-2,-3],
                            [9, 6, 2,6],
                            [0,-5,1,-5],
                            [0, 0, 0,0]])
        self.assertEqual(B.det(), 0)
        self.assertEqual(B.invertible(),False)

    def test_inverting(self):
        A = mytuple.Matrix([[-5,2,6,-8],
                            [1,-5,1,8],
                            [7,7,-6,-7],
                            [1,-3,7,4]])
        B = A.inverse()
        C = mytuple.Matrix([[ 0.21805, 0.45113, 0.24060,-0.04511],
                            [-0.80827,-1.45677,-0.44361, 0.52068],
                            [-0.07895,-0.22368,-0.05263, 0.19737],
                            [-0.52256,-0.81391,-0.30075, 0.30639]])
        self.assertEqual(A.det(), 532)

        self.assertEqual(A.cofactor(2,3), -160)
        self.assertEqual(math.isclose(B[3,2],-160/532), True)
        
        self.assertEqual(A.cofactor(3,2), 105)
        self.assertEqual(math.isclose(B[2,3], 105/532), True)
        
        self.assertEqual(C.equal(B.round()), True)

    def test_inverting2(self):
        A = mytuple.Matrix([[8,-5, 9,2],
                            [7, 5, 6,1],
                            [-6,0, 9,6],
                            [-3,0,-9,-4]])
        B = A.inverse()
        C = mytuple.Matrix([[-0.15385,-0.15385,-0.28205,-0.53846],
                            [-0.07692, 0.12308, 0.02564, 0.03077],
                            [0.35897, 0.35897, 0.43590, 0.92308],
                            [-0.69231,-0.69231,-0.76923,-1.92308]])
        self.assertEqual(C.equal(B.round()), True)

        A2 = mytuple.Matrix([[9, 3, 0, 9],
                             [-5,-2,-6,-3],
                             [-4,9,6,4],
                             [-7,6,6,2]])
        C2= mytuple.Matrix([[-0.04074, -0.07778, 0.14444, -0.22222],
                            [-0.07778, 0.03333, 0.36667, -0.33333],
                            [-0.02901, -0.14630, -0.10926, 0.12963],
                            [0.17778, 0.06667, -0.26667, 0.33333]])
        assert(C.equal(A.inverse().round()))

    def test_multinverse(self):
        A = mytuple.Matrix([[3,-9,7,3],
                            [3,-8,2,-9],
                            [-4,4,4,1],
                            [-6,5,-1,1]])
        B = mytuple.Matrix([[8,2,2,2],
                            [3,-1,7,0],
                            [7,0,5,4],
                            [6,-2,0,5]])
        C = A*B
        assert(A.equal(C*(B.inverse())))




class Transformationstest(unittest.TestCase):

    def test_translation(self):
        tran = mytuple.Matrix.translation(5,-3,2)
        p = mytuple.Point(-3,4,5)
        
        self.assertEqual( tran*p, mytuple.Point(2,1,7))

        inv = tran.inverse()
        self.assertEqual(inv*p, mytuple.Point(-8,7,3))

        v = mytuple.Vector(-3,4,5)
        self.assertEqual(tran*v, v)  #doesn't change vectors

    def test_scaling(self):
        transf = mytuple.Matrix.scaling(2,3,4)
        p = mytuple.Point(-4,6,8)
        v = mytuple.Vector(-4,6,8)

        self.assertEqual( transf*p, mytuple.Point(-8,18,32))
        self.assertEqual( transf*v, mytuple.Vector(-8,18,32)) #acting on vectors

        inv = transf.inverse()
        self.assertEqual( inv*v, mytuple.Vector(-2,2,2))

    def test_reflection(self):
        transf = mytuple.Matrix.scaling(-1,1,1)
        p = mytuple.Point(2,3,4)

        self.assertEqual(transf*p, mytuple.Point(-2,3,4))

        
    def test_xrotation(self):
        p = mytuple.Point(0,1,0)
        halfquarter = mytuple.Matrix.xrotation(math.pi /4)
        fullquarter = mytuple.Matrix.xrotation(math.pi /2)

        self.assertEqual(halfquarter*p, mytuple.Point(0,math.sqrt(2)/2, math.sqrt(2)/2))
        self.assertEqual(fullquarter*p, mytuple.Point(0,0,1))

        inv = halfquarter.inverse()
        self.assertEqual(inv*p,  mytuple.Point(0,math.sqrt(2)/2,-math.sqrt(2)/2))

    def test_yrotation(self):
        p= mytuple.Point(0,0,1)
        halfquarter = mytuple.Matrix.yrotation(math.pi /4)
        fullquarter = mytuple.Matrix.yrotation(math.pi /2)

        self.assertEqual(halfquarter*p, mytuple.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2))
        self.assertEqual(fullquarter*p, mytuple.Point(1,0,0))

    def test_zrotation(self):
        p= mytuple.Point(0,1,0)
        halfquarter = mytuple.Matrix.zrotation(math.pi /4)
        fullquarter = mytuple.Matrix.zrotation(math.pi /2)

        self.assertEqual(halfquarter*p , mytuple.Point(- math.sqrt(2)/2, math.sqrt(2)/2,0))
        self.assertEqual(fullquarter*p , mytuple.Point(-1,0,0))


        
    def test_shear(self):
        p = mytuple.Point(2,3,4)

        #x changes
        tr = mytuple.Matrix.shear(1,0,0, 0,0,0)
        self.assertEqual(tr*p , mytuple.Point(5,3,4))
        
        tr = mytuple.Matrix.shear(0,1,0, 0,0,0)
        self.assertEqual(tr*p , mytuple.Point(6,3,4))
        #y changes
        tr = mytuple.Matrix.shear(0,0,1, 0,0,0)
        self.assertEqual(tr*p , mytuple.Point(2,5,4))

        tr = mytuple.Matrix.shear(0,0,0, 1,0,0)
        self.assertEqual(tr*p , mytuple.Point(2,7,4))
        #z changes
        tr = mytuple.Matrix.shear(0,0,0, 0,1,0)
        self.assertEqual(tr*p , mytuple.Point(2,3,6))

        tr = mytuple.Matrix.shear(0,0,0, 0,0,1)
        self.assertEqual(tr*p , mytuple.Point(2,3,7))

    def test_chainedtransf(self):
        p = mytuple.Point(1,0,1)
        A = mytuple.Matrix.xrotation(math.pi/2)
        B = mytuple.Matrix.scaling(5,5,5)
        C = mytuple.Matrix.translation(10,5,7)

        p2 = A*p
        self.assertEqual(p2, mytuple.Point(1,-1,0))
        p3 = B*p2
        self.assertEqual(p3, mytuple.Point(5,-5,0))
        p4 = C*p3
        self.assertEqual(p4, mytuple.Point(15,0,7))

        T = C*B*A
        # T = mytuple.Matrix.Id().xrotation(math.pi/2).scaling(5,5,5).translation(10,5,7)
        self.assertEqual(T*p, mytuple.Point(15,0,7))







class RayTest(unittest.TestCase):

    def test_createray(self):
        origin = mytuple.Point(1,2,3)
        direction = mytuple.Vector(4,5,6)
        r = mytuple.ray(origin,direction)

        self.assertEqual(r.origin, origin)
        self.assertEqual(r.direction, direction)

    def test_computepoint(self):
        r = mytuple.ray(mytuple.Point(2,3,4), mytuple.Vector(1,0,0))

        self.assertEqual(r.position(0),  mytuple.Point(2, 3, 4))
        self.assertEqual(r.position(1),  mytuple.Point(3, 3, 4))
        self.assertEqual(r.position(-1), mytuple.Point(1, 3, 4))
        self.assertEqual(r.position(2.5), mytuple.Point(4.5, 3, 4))

        
    def test_inters2points(self):
        r = mytuple.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 4.0)
        self.assertEqual(xs[1].t, 6.0)

    def test_inters1tangent(self):
        r = mytuple.ray(mytuple.Point(0,1,-5), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 5.0)
        self.assertEqual(xs[1].t, 5.0)

    def test_inters0(self):
        r = mytuple.ray(mytuple.Point(0,2,-5), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 0)

    def test_inters_inside(self):
        r = mytuple.ray(mytuple.Point(0,0,0), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t,-1.0)
        self.assertEqual(xs[1].t, 1.0)

    def test_inters_behind(self):
        r = mytuple.ray(mytuple.Point(0,0,5), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, -6.0)
        self.assertEqual(xs[1].t, -4.0)

        
    def test_intersection(self):
        s = mytuple.sphere()
        
        i = mytuple.intersection(3.5, s)
        self.assertEqual(i.t, 3.5)
        self.assertEqual(i.obj, s)

    def test_aggregateintersections(self):
        s = mytuple.sphere()
        i1 = mytuple.intersection(1, s)
        i2 = mytuple.intersection(2, s)
        xs = mytuple.intersections(i1,i2) #no sense?

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t , 1)
        self.assertEqual(xs[1].t , 2)

    def test_inters_setobj(self):
        r = mytuple.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        s = mytuple.sphere()
        xs = r.inters(s)

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].obj , s)
        self.assertEqual(xs[1].obj , s)

        
    def test_hit_positive(self):
        s = mytuple.sphere()
        i1 = mytuple.intersection(1, s)
        i2 = mytuple.intersection(2, s)
        xs = mytuple.intersections(i2,i1)
        i = mytuple.hit(xs)

        self.assertEqual(i, i1)

    def test_hit1pos1neg(self):
        s = mytuple.sphere()
        i1 = mytuple.intersection(-1, s)
        i2 = mytuple.intersection(1, s)
        xs = mytuple.intersections(i2,i1)
        i = mytuple.hit(xs)

        self.assertEqual(i, i2)

    def test_hit_negative(self):
        s = mytuple.sphere()
        i1 = mytuple.intersection(-2, s)
        i2 = mytuple.intersection(-1, s)
        xs = mytuple.intersections(i2,i1)
        i = mytuple.hit(xs)

        self.assertEqual(i, None)

    def test_hitmultiple(self):
        s = mytuple.sphere()
        i1 = mytuple.intersection(5, s)
        i2 = mytuple.intersection(7, s)
        i3 = mytuple.intersection(-3, s)
        i4 = mytuple.intersection(2, s)
        xs = mytuple.intersections(i1,i2,i3,i4)

        self.assertEqual(mytuple.hit(xs), i4)

    def test_raytransform(self):
        r = mytuple.ray(mytuple.Point(1,2,3), mytuple.Vector(0,1,0))
        m = mytuple.Matrix.translation(3,4,5)
        r2 = r.transform(m)

        self.assertEqual(r2.origin,    mytuple.Point(4,6,8))
        self.assertEqual(r2.direction, mytuple.Vector(0,1,0))

        m = mytuple.Matrix.scaling(2,3,4)
        r2 = r.transform(m)

        self.assertEqual(r2.origin,    mytuple.Point(2,6,12))
        self.assertEqual(r2.direction, mytuple.Vector(0,3,0))

    def test_spheretransform(self):
        s = mytuple.sphere()
        assert(mytuple.Matrix.equal(s.transform, mytuple.Matrix.Id()))

        t= mytuple.Matrix.translation(2,3,4)
        s.settransform(t)
        assert(t.equal(s.transform))

    def test_inters_transformedray(self):
        s = mytuple.sphere()
        r = mytuple.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))

        s.settransform(mytuple.Matrix.scaling(2,2,2)) # scaled sphere
        xs = r.inters(s)
        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t, 3)
        self.assertEqual(xs[1].t, 7)

        s.settransform(mytuple.Matrix.translation(5,0,0)) # translated sphere
        xs = r.inters(s)
        self.assertEqual(len(xs), 0)


class TestShading(unittest.TestCase):

    def test_normal(self):
        s = mytuple.sphere()
        n = s.normal(mytuple.Point(1,0,0))
        self.assertEqual(n, mytuple.Vector(1,0,0))

        n = s.normal(mytuple.Point(0,1,0))
        self.assertEqual(n, mytuple.Vector(0,1,0))

        n = s.normal(mytuple.Point(0,0,1))
        self.assertEqual(n, mytuple.Vector(0,0,1))

        n = s.normal(mytuple.Point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3 ))
        self.assertEqual(n, mytuple.Vector(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))

    def test_normalnorm(self):
        s = mytuple.sphere()
        p = mytuple.Point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3 )
        n= s.normal( p)

        self.assertEqual(n, n.normalize())

    def test_transformednormal(self):
        s= mytuple.sphere()
        s.settransform(mytuple.Matrix.translation(0,1,0))
        n = s.normal(mytuple.Point(0, 1.70711, -0.70711))

        self.assertEqual(n.round(), mytuple.Vector(0, 0.70711, -0.70711))

        #s = mytuple.sphere()
        m = mytuple.Matrix.scaling(1, .5, 1) * mytuple.Matrix.zrotation(math.pi /5)
        s.settransform(m)
        n = s.normal(mytuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))

        self.assertEqual(n.round(), mytuple.Vector(0, .97014, -0.24254))

    def test_reflection(self):
        v = mytuple.Vector(1,-1,0)
        n = mytuple.Vector(0,1,0)
        r = v.reflect(n)
        self.assertEqual(r, mytuple.Vector(1,1,0))

        v = mytuple.Vector(0,-1,0)
        n = mytuple.Vector(math.sqrt(2) /2, math.sqrt(2) /2, 0)
        r = v.reflect(n)
        self.assertEqual(r, mytuple.Vector(1,0,0))
        
