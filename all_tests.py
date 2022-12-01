import unittest
import math

import mytuple
import mycolor
import myworld

class TupleTest(unittest.TestCase):  #1

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

    
    

class ColorTest(unittest.TestCase): #2
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



        

class CanvasTest(unittest.TestCase): #2.2
    
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








        


class Matrixtest(unittest.TestCase): #3

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

        self.assertTrue(A.equal(B))

    def test_notequalmatrix(self):
        A = mytuple.Matrix([[1,2,3,4],
                            [5,6,7,8],
                            [9,8,7,6],
                            [5,4,3,2]])
        B = mytuple.Matrix([[2,3,4,5],
                            [6,7,8,9],
                            [8,7,6,5],
                            [4,3,2,1]])

        self.assertFalse(A.equal(B))

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
        self.assertTrue( C.equal(A*B))

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

        self.assertTrue(A.equal(A* mytuple.Matrix.Id()))

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
        self.assertTrue(A.transpose().equal(B))
        self.assertTrue(C.equal(mytuple.Matrix.Id()))

        
    def test_2x2determinant(self):
        A = mytuple.Matrix([[1,5],[-3,2]])

        self.assertAlmostEqual(A.det(), 17)
        
    def test_submatrix(self):
        A= mytuple.Matrix([[ 1,5,0],
                           [-3,2,7],
                           [ 0,6,-3]])
        self.assertTrue(A.submatrix(0,2).equal(mytuple.Matrix([[-3,2],
                                                                [0,6]])))
        B= mytuple.Matrix([[-6,1, 1,6],
                           [-8,5, 8,6],
                           [-1,0, 8,2],
                           [-7,1,-1,1]])
        self.assertTrue(B.submatrix(2,1).equal(mytuple.Matrix([[-6, 1,6],
                                                               [-8, 8,6],
                                                               [-7,-1,1]])))
    def test_minor_cofactor(self):
        A= mytuple.Matrix([[3, 5,0],
                           [2,-1,-7],
                           [6,-1,5]])
        B = A.submatrix(1,0)
        
        self.assertAlmostEqual(B.det(), 25)
        self.assertAlmostEqual(A.minor(1,0), 25)

        self.assertAlmostEqual(A.cofactor(1,0),-25)

        self.assertAlmostEqual(A.minor(0,0),  -12)
        self.assertAlmostEqual(A.cofactor(0,0),-12)
        
    def test_3x3determinant(self):
        A = mytuple.Matrix([[1, 2,6],
                            [-5,8,-4],
                            [2, 6, 4]])
        self.assertAlmostEqual(A.cofactor(0,0), 56)
        self.assertAlmostEqual(A.cofactor(0,1), 12)
        self.assertAlmostEqual(A.cofactor(0,2),-46)

        self.assertAlmostEqual(A.det(),-196)

    def test_4x4determinant(self):
        A = mytuple.Matrix([[-2,-8,3,5],
                            [-3, 1,7,3],
                            [1, 2,-9,6],
                            [-6,7,7,-9]])
        self.assertAlmostEqual(A.cofactor(0,0), 690)
        self.assertAlmostEqual(A.cofactor(0,1), 447)
        self.assertAlmostEqual(A.cofactor(0,2), 210)
        self.assertAlmostEqual(A.cofactor(0,3), 51)

        self.assertAlmostEqual(A.det(),-4071)

    def test_isinvertible(self):
        A = mytuple.Matrix([[6,4,4,4],
                            [5,5,7,6],
                            [4,-9,3,-7],
                            [9,1,7,-6]])
        self.assertAlmostEqual(A.det(),-2120)
        self.assertTrue(A.invertible())
        
        B = mytuple.Matrix([[-4,2,-2,-3],
                            [9, 6, 2,6],
                            [0,-5,1,-5],
                            [0, 0, 0,0]])
        self.assertAlmostEqual(B.det(), 0)
        self.assertFalse(B.invertible())

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
        self.assertAlmostEqual(A.det(), 532)

        self.assertAlmostEqual(A.cofactor(2,3), -160)
        self.assertTrue(math.isclose(B[3,2],-160/532))
        
        self.assertAlmostEqual(A.cofactor(3,2), 105)
        self.assertTrue(math.isclose(B[2,3], 105/532))
        
        self.assertTrue(C.equal(B.round()))

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
        self.assertTrue(C.equal(B.round()))

        A2 = mytuple.Matrix([[9, 3, 0, 9],
                             [-5,-2,-6,-3],
                             [-4,9,6,4],
                             [-7,6,6,2]])
        C2= mytuple.Matrix([[-0.04074,-0.07778, 0.14444, -0.22222],
                            [-0.07778, 0.03333, 0.36667, -0.33333],
                            [-0.02901,-0.14630, -0.10926, 0.12963],
                            [ 0.17778, 0.06667, -0.26667, 0.33333]])
        self.assertTrue(C2.equal( A2.inverse().round() ))

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
        self.assertTrue(A.equal( C*(B.inverse()) ))

        


        

class Transformationstest(unittest.TestCase): #4

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







class RayTest(unittest.TestCase): #5

    def test_createray(self):
        origin = mytuple.Point(1,2,3)
        direction = mytuple.Vector(4,5,6)
        r = myworld.ray(origin,direction)

        self.assertEqual(r.origin, origin)
        self.assertEqual(r.direction, direction)



    def test_computepoint(self):
        r = myworld.ray(mytuple.Point(2,3,4), mytuple.Vector(1,0,0))

        self.assertEqual(r.position(0),  mytuple.Point(2, 3, 4))
        self.assertEqual(r.position(1),  mytuple.Point(3, 3, 4))
        self.assertEqual(r.position(-1), mytuple.Point(1, 3, 4))
        self.assertEqual(r.position(2.5), mytuple.Point(4.5, 3, 4))

        
    def test_inters2points(self):  #modif. localintersect
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].t, 4.0)
        self.assertAlmostEqual(xs[1].t, 6.0)

    def test_inters1tangent(self): #modif. localintersect
        r = myworld.ray(mytuple.Point(0,1,-5), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].t, 5.0)
        self.assertAlmostEqual(xs[1].t, 5.0)

    def test_inters0(self): #modif. localintersect
        r = myworld.ray(mytuple.Point(0,2,-5), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 0)

    def test_inters_inside(self): #modif. localintersect
        r = myworld.ray(mytuple.Point(0,0,0), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].t,-1.0)
        self.assertAlmostEqual(xs[1].t, 1.0)

    def test_inters_behind(self): #modif. localintersect
        r = myworld.ray(mytuple.Point(0,0,5), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].t, -6.0)
        self.assertAlmostEqual(xs[1].t, -4.0)


        
    def test_intersection(self):
        s = myworld.sphere()
        
        i = myworld.intersection(3.5, s)
        self.assertAlmostEqual(i.t, 3.5)
        self.assertEqual(i.obj, s)

    def test_aggregateintersections(self):
        s = myworld.sphere()
        i1 = myworld.intersection(1, s)
        i2 = myworld.intersection(2, s)
        xs = myworld.intersections(i1,i2) #no sense?

        self.assertEqual(len(xs), 2)
        self.assertEqual(xs[0].t , 1)
        self.assertEqual(xs[1].t , 2)

    def test_inters_obj(self): #modif. localintersect
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        s = myworld.sphere()
        xs = s.localintersect(r)

        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].obj , s)
        self.assertAlmostEqual(xs[1].obj , s)

        
    def test_hit_positive(self):
        s = myworld.sphere()
        i1 = myworld.intersection(1, s)
        i2 = myworld.intersection(2, s)
        xs = myworld.intersections(i2,i1)
        i = myworld.hit(xs)

        self.assertEqual(i, i1)

    def test_hit1pos1neg(self):
        s = myworld.sphere()
        i1 = myworld.intersection(-1, s)
        i2 = myworld.intersection(1, s)
        xs = myworld.intersections(i2,i1)
        i = myworld.hit(xs)

        self.assertEqual(i, i2)

    def test_hit_negative(self):
        s = myworld.sphere()
        i1 = myworld.intersection(-2, s)
        i2 = myworld.intersection(-1, s)
        xs = myworld.intersections(i2,i1)
        i = myworld.hit(xs)

        self.assertEqual(i, None)

    def test_hitmultiple(self):
        s = myworld.sphere()
        i1 = myworld.intersection(5, s)
        i2 = myworld.intersection(7, s)
        i3 = myworld.intersection(-3, s)
        i4 = myworld.intersection(2, s)
        xs = myworld.intersections(i1,i2,i3,i4)

        self.assertEqual(myworld.hit(xs), i4)

    def test_raytransform(self):
        r = myworld.ray(mytuple.Point(1,2,3), mytuple.Vector(0,1,0))
        m = mytuple.Matrix.translation(3,4,5)
        r2 = r.transform(m)

        self.assertEqual(r2.origin,    mytuple.Point(4,6,8))
        self.assertEqual(r2.direction, mytuple.Vector(0,1,0))

        m = mytuple.Matrix.scaling(2,3,4)
        r2 = r.transform(m)

        self.assertEqual(r2.origin,    mytuple.Point(2,6,12))
        self.assertEqual(r2.direction, mytuple.Vector(0,3,0))

    # def test_spheretransformation(self):
    #     s = myworld.sphere()
    #     self.assertTrue(mytuple.Matrix.equal(s.transformation, mytuple.Matrix.Id()))

    #     t= mytuple.Matrix.translation(2,3,4)
    #     s.settransform(t)
    #     self.assertTrue(t.equal(s.transformation))

    def test_inters_transformedsphere(self):  #non cambiato
        s = myworld.sphere()
        r = myworld.ray( mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))

        s.settransform(mytuple.Matrix.scaling(2,2,2)) # scaled sphere
        xs = r.inters(s)
        self.assertEqual(len(xs), 2)
        self.assertAlmostEqual(xs[0].t, 3)
        self.assertAlmostEqual(xs[1].t, 7)

        s.settransform(mytuple.Matrix.translation(5,0,0)) # translated sphere
        xs = r.inters(s)
        self.assertEqual(len(xs), 0)





        
class TestShading(unittest.TestCase): #6

    def test_normal_at(self):  #modif. localnormal_at
        s = myworld.sphere()
        n = s.localnormal_at(mytuple.Point(1,0,0))
        self.assertEqual(n, mytuple.Vector(1,0,0))

        n = s.localnormal_at(mytuple.Point(0,1,0))
        self.assertEqual(n, mytuple.Vector(0,1,0))

        n = s.localnormal_at(mytuple.Point(0,0,1))
        self.assertEqual(n, mytuple.Vector(0,0,1))

        n = s.localnormal_at(mytuple.Point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3 ))
        self.assertEqual(n, mytuple.Vector(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3))

    def test_normalnorm(self): #modif. localnormal_at
        s = myworld.sphere()
        p = mytuple.Point(math.sqrt(3)/3, math.sqrt(3)/3, math.sqrt(3)/3 )
        n= s.localnormal_at( p)

        self.assertEqual(n, n.normalize())

    # def test_transformednormal(self):
    #     s= myworld.sphere()
    #     s.settransform(mytuple.Matrix.translation(0,1,0))
    #     n = s.normal_at(mytuple.Point(0, 1.70711, -0.70711))

    #     self.assertEqual(n.round(), mytuple.Vector(0, 0.70711, -0.70711)) #translated sphere

    #     #s = myworld.sphere()
    #     m = mytuple.Matrix.scaling(1, .5, 1) * mytuple.Matrix.zrotation(math.pi /5)
    #     s.settransform(m)
    #     n = s.normal_at(mytuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))

    #     self.assertEqual(n.round(), mytuple.Vector(0, .97014, -0.24254)) # transformed sphere

    def test_reflection(self):
        v = mytuple.Vector(1,-1,0)
        n = mytuple.Vector(0,1,0)
        r = v.reflect(n)
        self.assertEqual(r, mytuple.Vector(1,1,0))

        v = mytuple.Vector(0,-1,0)
        n = mytuple.Vector(math.sqrt(2) /2, math.sqrt(2) /2, 0)
        r = v.reflect(n)
        self.assertEqual(r, mytuple.Vector(1,0,0))

    def test_pointlight(self):
        intensity= mycolor.Color(1,1,1)
        position = mytuple.Point(0,0,0)
        l = myworld.pointlight(position,intensity)

        self.assertAlmostEqual(l.position, position)
        self.assertAlmostEqual(l.intensity, intensity)

    def test_material(self):
        m = myworld.Material()

        self.assertEqual(m.color, mycolor.Color(1,1,1))
        self.assertEqual(m.ambient, .1)
        self.assertEqual(m.diffuse, .9)
        self.assertEqual(m.specular, .9)
        self.assertEqual(m.shininess, 200.0)

    # def test_spherematerial(self):
    #     s = myworld.sphere()
    #     self.assertTrue( s.material.equal(myworld.Material() ))
    #     # è quello default, equality not identity

    #     m = myworld.Material()
    #     m.ambient = 1
    #     s.material = m
    #     self.assertEqual(s.material, m)  #here it works (bruh)

    #LIGHTING

    def test_lighting1front(self):
        m = myworld.Material()
        position = mytuple.Point(0,0,0)
        
        eye = mytuple.Vector(0,0,-1)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,0,-10), mycolor.Color(1,1,1))
        result = myworld.lighting(m, light, position, eye, normal)

        self.assertTrue(result == mycolor.Color(1.9, 1.9, 1.9))

    def test_lighting2middle(self):
        m = myworld.Material()
        position = mytuple.Point(0,0,0)
        
        eye = mytuple.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,0,-10), mycolor.Color(1,1,1))
        result = myworld.lighting(m, light, position, eye, normal)

        self.assertTrue(result == mycolor.Color(1, 1, 1))

    def test_lighting3above(self):
        m = myworld.Material()
        position = mytuple.Point(0,0,0)
        
        eye = mytuple.Vector(0,0,-1)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,10,-10), mycolor.Color(1,1,1))
        result = myworld.lighting(m, light, position, eye, normal)

        self.assertTrue(result.round5() == mycolor.Color(.7364, .7364, .7364 ))

    def test_lighting4above(self):
        m = myworld.Material()
        position = mytuple.Point(0,0,0)

        eye = mytuple.Vector(0, -math.sqrt(2)/2, -math.sqrt(2)/2)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,10,-10), mycolor.Color(1,1,1))
        result = myworld.lighting(m, light, position, eye, normal)
        
        self.assertTrue(result.round5() == mycolor.Color(1.6364, 1.6364, 1.6364))

    def test_lighting5behind(self):
        m = myworld.Material()
        position = mytuple.Point(0,0,0)

        eye = mytuple.Vector(0, 0, -1)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,0,10), mycolor.Color(1,1,1))
        result = myworld.lighting(m, light, position, eye, normal)
        
        self.assertTrue(result.round5() == mycolor.Color(.1, .1, .1))
    


        

#CHAPTER 7 ############################################################################
class TestWorld(unittest.TestCase):

    def test_emptyworld(self):
        w = myworld.World()

        self.assertFalse(w.obj)
        self.assertFalse(w.lightsource)

    def test_default(self):
        l = myworld.pointlight(mytuple.Point(-10,10,-10), mycolor.Color(1,1,1))
        s1 = myworld.sphere()
        s1.material.color = mycolor.Color(0.8, 1.0, 0.6)
        s1.material.diffuse = 0.7
        s1.material.specular= 0.2

        s2 = myworld.sphere()
        s2.transformation = mytuple.Matrix.scaling(.5, .5, .5)

        w = myworld.World.defaultworld()
        self.assertTrue( myworld.pointlight.equal(w.lightsource, l))

        # filter is not empty if s1.equal(elem) for some elem in w.obj
        self.assertTrue( filter(s1.equal, w.obj) )
        self.assertTrue( filter(s2.equal, w.obj))

    def test_worldray(self):
        w = myworld.World.defaultworld()
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        xs = w.intersectworld(r)

        self.assertTrue(len(xs)==4)
        self.assertAlmostEqual(xs[0].t, 4)
        self.assertAlmostEqual(xs[1].t, 4.5)
        self.assertAlmostEqual(xs[2].t, 5.5)
        self.assertAlmostEqual(xs[3].t, 6)

    def test_precomputeinters(self):
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        shape = myworld.sphere()
        i = myworld.intersection(4, shape)
        comps = myworld.precomp(i, r)
        
        self.assertEqual(comps["t"], i.t)
        self.assertEqual(comps["obj"], i.obj)
        self.assertEqual(comps["point"], mytuple.Point(0,0,-1))
        self.assertEqual(comps["eyev"], mytuple.Vector(0,0,-1))
        self.assertEqual(comps["normal"], mytuple.Vector(0,0,-1))

    def test_outsidehit(self):
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        shape = myworld.sphere()
        i = myworld.intersection(4, shape)
        comps = myworld.precomp(i, r)

        self.assertFalse(comps["inside"])

    def test_insidehit(self):
        r = myworld.ray(mytuple.Point(0,0,0), mytuple.Vector(0,0,1))
        shape = myworld.sphere()
        i = myworld.intersection(1, shape)
        comps = myworld.precomp(i, r)

        self.assertTrue(comps["point"]== mytuple.Point(0,0,1))
        self.assertTrue(comps["eyev"] == mytuple.Vector(0,0,-1))
        self.assertTrue(comps["inside"])
        self.assertTrue(comps["normal"]== mytuple.Vector(0,0,-1))

    def test_shade_hit_outside(self):
        w = myworld.World.defaultworld()
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        shape = w.obj[0]
        i = myworld.intersection(4, shape)
        comps = myworld.precomp(i, r)
        
        c = w.shade_hit(comps)
        self.assertTrue(c.round5() ==mycolor.Color(0.38066, 0.47583, 0.2855))

    def test_shadehit_inside(self):
        w = myworld.World.defaultworld()
        w.lightsource = myworld.pointlight(mytuple.Point(0, .25, 0), mycolor.Color(1,1,1))
        
        r = myworld.ray(mytuple.Point(0,0,0), mytuple.Vector(0,0,1))
        shape = w.obj[1]
        i = myworld.intersection(.5, shape)
        comps = myworld.precomp(i, r)
        
        c = w.shade_hit(comps)
        self.assertTrue(c.round5() == mycolor.Color(.90498, .90498, .90498))


    def test_colorat(self):
        w = myworld.World.defaultworld()

        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,1,0))
        c = w.colorat(r)
        self.assertEqual(c, mycolor.Color(0,0,0))

        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        c = w.colorat(r)
        self.assertEqual(c.round5(), mycolor.Color(0.38066, 0.47583, 0.2855))

    def test_colorat_usehit(self):
        w = myworld.World.defaultworld()
        r = myworld.ray(mytuple.Point(0,0,.75), mytuple.Vector(0,0,-1))
        outer = w.obj[0]
        outer.material.ambient = 1
        inner = w.obj[1]
        inner.material.ambient = 1

        self.assertTrue(w.colorat(r) == inner.material.color)
        



class TestView(unittest.TestCase):

    def test_viewdefaultorientation(self):
        from0 = mytuple.Point(0,0,0) # 'from' non si può usare 
        to = mytuple.Point(0,0,-1)
        up = mytuple.Vector(0,1,0)
        #default
        t = mytuple.Matrix.viewtransform(from0, to, up)
        self.assertTrue(t.equal( mytuple.Matrix.Id()))

        from0 = mytuple.Point(0,0,0)
        to = mytuple.Point(0,0,1)
        up = mytuple.Vector(0,1,0)

        t= mytuple.Matrix.viewtransform(from0,to,up)
        self.assertTrue(t.equal( mytuple.Matrix.scaling(-1,1,-1)))

    def test_viewmovesworld(self):
        from0 = mytuple.Point(0,0,8)
        to = mytuple.Point(0,0,0)
        up = mytuple.Vector(0,1,0)

        t= mytuple.Matrix.viewtransform(from0,to,up)
        self.assertTrue(t.equal(mytuple.Matrix.translation(0,0,-8)))

    def test_viewarbitrary(self):
        from0 = mytuple.Point(1,3,2)
        to = mytuple.Point(4,-2,8)
        up = mytuple.Vector(1,1,0)

        t = mytuple.Matrix.viewtransform(from0,to,up)
        self.assertTrue(t.round().equal(mytuple.Matrix([[-0.50709,0.50709, 0.67612,-2.36643],
                                                        [0.76772, 0.60609, 0.12122,-2.82843],
                                                [-0.35857,0.59761,-0.71714, 0],
                                                [ 0,      0,       0,       1]])))

        
    def test_buildcamera(self):
        hsize, vsize, field = 160, 120, math.pi/2
        c = myworld.Camera(hsize, vsize, field)
        
        self.assertEqual(c.hsize, 160)
        self.assertEqual(c.vsize, 120)
        self.assertAlmostEqual(c.field, math.pi/2)
        self.assertTrue(c.transformation.equal( mytuple.Matrix.Id()))

    def test_camera_pixelsize(self):
        c = myworld.Camera(200, 125, math.pi/2)
        self.assertAlmostEqual(c.pixelsize, 0.01) #almost

        c = myworld.Camera(125,200,math.pi/2)
        self.assertAlmostEqual(c.pixelsize, 0.01)

    def test_raytocenterorcorner(self):
        c = myworld.Camera(201, 101, math.pi/2)
        r = myworld.Camera.rayforpixel(c,100,50)

        self.assertEqual(r.origin, mytuple.Point(0,0,0))
        self.assertEqual(r.direction, mytuple.Vector(0,0,-1))

        r = myworld.Camera.rayforpixel(c, 0,0)
        self.assertEqual(r.origin, mytuple.Point(0,0,0))
        self.assertEqual(r.direction.round(), mytuple.Vector(0.66519, 0.33259, -0.66851))

    def test_rayforpixel_transformed(self):
        c = myworld.Camera(201, 101, math.pi/2)
        c.transformation = mytuple.Matrix.yrotation(math.pi/4) * mytuple.Matrix.translation(0,-2,5)
        r = myworld.Camera.rayforpixel(c,100,50)

        self.assertEqual(r.origin, mytuple.Point(0,2,-5))
        self.assertEqual(r.direction, mytuple.Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2))

    def test_render(self):
        w = myworld.World.defaultworld()
        c = myworld.Camera(11,11, math.pi/2)
        from_ = mytuple.Point(0,0,-5)
        to = mytuple.Point(0,0,0)
        up = mytuple.Vector(0,1,0)
        c.transformation = mytuple.Matrix.viewtransform(from_,to,up)

        image = myworld.Camera.render(c, w)
        #mycolor.canvastoppm(image, "testrender.ppm")
        self.assertEqual(image[5,5].round5(), mycolor.Color(0.38066, 0.47583, 0.2855))
        




# # # CHAPTER 8 #############################################################################

class ShadowsTest(unittest.TestCase):

    def test_lighting_surfaceinshadow(self):
        #common background (p.86)
        m = myworld.Material()
        position = mytuple.Point(0,0,0)
        
        eye = mytuple.Vector(0,0,-1)
        normal = mytuple.Vector(0,0,-1)
        light = myworld.pointlight(mytuple.Point(0,0,-10), mycolor.Color(1,1,1))
        inshadow = True
        result = myworld.lighting(m, light, position, eye, normal, inshadow)
        
        self.assertEqual(result, mycolor.Color(0.1, 0.1, 0.1))

    def test_notinshadow_notcollinear(self):
        w = myworld.World.defaultworld()
        p = mytuple.Point(0,10,0)
        self.assertFalse( w.isinshadow(p))

    def test_inshadow_objbetween(self):
        w = myworld.World.defaultworld()
        p = mytuple.Point(10,-10,10)
        self.assertTrue( w.isinshadow(p))

    def test_notinshadow_objbehindlight(self):
        w = myworld.World.defaultworld()
        p = mytuple.Point(-20,20,-20)
        self.assertFalse( w.isinshadow(p))

    def test_notinshadow_objbehindpoint(self):
        w = myworld.World.defaultworld()
        p = mytuple.Point(-2,2,-2)
        self.assertFalse( w.isinshadow(p))

    #change World.shade_hit()
    def test_shadehit_inshadow(self):
        w = myworld.World()
        w.lightsource = myworld.pointlight(mytuple.Point(0,0,-10), mycolor.Color(1,1,1))
        s1 = myworld.sphere()
        s2 = myworld.sphere()
        s2.transformation = mytuple.Matrix.translation(0,0,10)
        w.obj = [s1, s2]
        r = myworld.ray(mytuple.Point(0,0,5), mytuple.Vector(0,0,1))
        i = myworld.intersection(4, s2)

        comps= myworld.precomp(i,r)
        c = w.shade_hit(comps)
        self.assertEqual(c, mycolor.Color(0.1, 0.1, 0.1))
        # funziona ma visivamente fa acne sull'immagine

    def test_thehit_offsetthepoint(self): #evitare acne
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))
        shape = myworld.sphere()
        shape.transformation = mytuple.Matrix.translation(0,0,1)
        i = myworld.intersection(5, shape)
        comps = myworld.precomp(i,r)

        self.assertLess( comps['pointover'].z , -mytuple.EPSILON/2)
        self.assertLess( comps['pointover'].z , comps['point'].z)






# CHAP 9 #################################################################################
class TestPlanes(unittest.TestCase):

    def test_shapetransformation(self):
        s = myworld.Shape()
        self.assertTrue(s.transformation.equal( mytuple.Matrix.Id()))

        s.settransform( mytuple.Matrix.translation(2,3,4))
        self.assertTrue(s.transformation.equal( mytuple.Matrix.translation(2,3,4)))

    def test_shapematerial(self):
        S = myworld.Shape()
        m = S.material                     #unica riga?
        self.assertTrue(m.equal( myworld.Material()))  #the default material

        s = myworld.Shape()
        m = myworld.Material()
        m.ambient = 1
        s.material = m
        self.assertTrue(s.material.equal( m))

    def test_shape_localinters(self):
        s = myworld.Shape()
        r = myworld.ray(mytuple.Point(0,0,-5), mytuple.Vector(0,0,1))

        s.settransform(mytuple.Matrix.scaling(2,2,2)) # scaled shape
        xs = r.inters(s)
        self.assertEqual(s.savedray.origin,   mytuple.Point(0,0,-2.5))
        self.assertEqual(s.savedray.direction, mytuple.Vector(0,0, 0.5))
        
        s.settransform(mytuple.Matrix.translation(5,0,0)) # translated shape
        xs = r.inters(s)
        self.assertEqual(s.savedray.origin,   mytuple.Point(-5,0,-5))
        self.assertEqual(s.savedray.direction, mytuple.Vector(0,0,1))

    def test_shape_transformednormal_at(self):
        s= myworld.Shape()
        s.settransform( mytuple.Matrix.translation(0,1,0))
        n = s.normal_at(mytuple.Point(0, 1.70711, -0.70711))
        self.assertEqual(n.round(), mytuple.Vector(0, 0.70711, -0.70711)) #translated shape

        #s = myworld.Shape()
        m = mytuple.Matrix.scaling(1, .5, 1) * mytuple.Matrix.zrotation(math.pi /5)
        s.settransform(m)
        n = s.normal_at(mytuple.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
        self.assertEqual(n.round(), mytuple.Vector(0, .97014, -0.24254)) # transformed shape

    def test_sphereissubclassofShape(self):
        self.assertTrue(issubclass(myworld.sphere, myworld.Shape))


        
    def test_planenormal(self):
        p = myworld.Plane()
        n1 = p.localnormal_at(mytuple.Point(0,0,0))
        n2 = p.localnormal_at(mytuple.Point(10,0,-10))
        n3 = p.localnormal_at(mytuple.Point(-5,0,150))

        self.assertEqual(n1, mytuple.Vector(0,1,0))
        self.assertEqual(n2, mytuple.Vector(0,1,0))
        self.assertEqual(n3, mytuple.Vector(0,1,0))

    def test_plane_parallelray(self):
        p = myworld.Plane()
        r = myworld.ray(mytuple.Point(0,10,0), mytuple.Vector(0,0,1))
        xs = p.localintersect(r)
        self.assertEqual(xs, None)
    
    def test_plane_coplanarray(self):
        p = myworld.Plane()
        r = myworld.ray(mytuple.Point(0,0,0), mytuple.Vector(0,0,1))
        xs = p.localintersect(r)
        self.assertEqual(xs, None) #torna xk non esiste p.localinters

    def test_plane_fromabove(self):
        p = myworld.Plane()
        r = myworld.ray(mytuple.Point(0,1,0), mytuple.Vector(0,-1,0))
        xs = p.localintersect(r)

        self.assertEqual(len(xs), 1)
        self.assertAlmostEqual(xs[0].t, 1)
        self.assertEqual(xs[0].obj, p)
    
    def test_plane_fromabove(self):
        p = myworld.Plane()
        r = myworld.ray(mytuple.Point(0,-1,0), mytuple.Vector(0,1,0))
        xs = p.localintersect(r)
        
        self.assertEqual(len(xs), 1)
        self.assertAlmostEqual(xs[0].t, 1)
        self.assertEqual(xs[0].obj, p)





# CHAP 10 ##############################################################################
class TestPatterns(unittest.TestCase):

    def test_stripepattern(self):
        pattern = myworld.Stripepattern(mycolor.white(), mycolor.black())

        self.assertEqual(pattern.a, mycolor.white())
        self.assertEqual(pattern.b, mycolor.black())

    def test_stripe_at(self): #(stripe_at)
        pattern = myworld.Stripepattern(mycolor.white(), mycolor.black())

        self.assertEqual(pattern.stripe_at(mytuple.Point(0,0,0)), mycolor.white()) #in y
        self.assertEqual(pattern.stripe_at(mytuple.Point(0,1,0)), mycolor.white())
        self.assertEqual(pattern.stripe_at(mytuple.Point(0,2,0)), mycolor.white())
        
