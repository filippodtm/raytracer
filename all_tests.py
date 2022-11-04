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
        M = mytuple.Matrix(4,4)
        M[0,:] = [1,2,3,4]
        M[1,:] = [5.5, 6.5, 7.5, 8.5]
        M[2,:] = [9, 10, 11, 12]
        M[3,:] = [13.5, 14.5, 15.5, 16.5]
        #M[:,:] = [[1,2,3,4],[5.5, 6.5, 7.5, 8.5],[9,10,11,12],[13.5,14.5,15.5,16.5]]

        self.assertEqual(M[0,0], 1)
        self.assertEqual(M[0,3], 4)
        self.assertEqual(M[1,0], 5.5)
        self.assertEqual(M[1,2], 7.5)
        self.assertEqual(M[2,2], 11)
        self.assertEqual(M[3,0], 13.5)
        self.assertEqual(M[3,2], 15.5)
        

    def test_create2x2matrix(self):
        M = mytuple.Matrix(2,2)
        M[0,:] = [-3,5]
        M[1,:] = [1,-2]

        self.assertEqual(M[0,0], -3)
        self.assertEqual(M[0,1], 5)
        self.assertEqual(M[1,0], 1)
        self.assertEqual(M[1,1], -2)

    def test_create3x3matrix(self):
        M = mytuple.Matrix(3,3)
        M[0,:] = [-3,5, 0]
        M[1,:] = [1,-2,-7]
        M[2,:] = [0, 1, 1]

        self.assertEqual(M[0,0], -3)
        self.assertEqual(M[1,1], -2)
        self.assertEqual(M[2,2], 1)

    def test_equalmatrix(self):
        A = mytuple.Matrix(4,4)
        A[0,:] = [1,2,3,4]
        A[1,:] = [5,6,7,8]
        A[2,:] = [9,8,7,6]
        A[3,:] = [5,4,3,2]
        B = mytuple.Matrix(4,4)
        B[0,:] = [1,2,3,4]
        B[1,:] = [5,6,7,8]
        B[2,:] = [9,8,7,6]
        B[3,:] = [5,4,3,2]

        self.assertEqual(A==B, True)

    def test_differentmatrix(self):
        A = mytuple.Matrix(4,4)
        A[0,:] = [1,2,3,4]
        A[1,:] = [5,6,7,8]
        A[2,:] = [9,8,7,6]
        A[3,:] = [5,4,3,2]

        B = mytuple.Matrix(4,4)
        B[0,:] = [2,3,4,5]
        B[1,:] = [6,7,8,9]
        B[2,:] = [8,7,6,5]
        B[3,:] = [4,3,2,1]

        self.assertEqual(A!=B, True)

    def test_matrixmult(self):
        A = mytuple.Matrix(4,4)
        A[0,:] = [1,2,3,4]
        A[1,:] = [5,6,7,8]
        A[2,:] = [9,8,7,6]
        A[3,:] = [5,4,3,2]

        B = mytuple.Matrix(4,4)
        B[0,:] = [-2,1,2,3]
        B[1,:] = [3,2,1,-1]
        B[2,:] = [4,3,6,5]
        B[3,:] = [1,2,7,8]

        C = mytuple.Matrix(4,4)
        C[0,:] = [20,22,50,48]
        C[1,:] = [44,54,114,108]
        C[2,:] = [40,58,110,102]
        C[3,:] = [16,26,46,42]

        self.assertEqual(A*B, C)

    def test_matrixtuple(self):
        A = mytuple.Matrix(4,4)
        A[0,:] = [1,2,3,4]
        A[1,:] = [2,4,4,2]
        A[2,:] = [8,6,4,1]
        A[3,:] = [0,0,0,1]
        b = mytuple.MyTuple(1,2,3,1)
        c = mytuple.MyTuple(18,24,33,1)

        self.assertEqual(A*b, c)

    def test_matrixbyidentity(self):
        A = mytuple.Matrix(4,4)
        A[0,:] = [0,1,2,4]
        A[1,:] = [1,2,4,8]
        A[2,:] = [2,4,8,16]
        A[3,:] = [4,8,16,32]

        self.assertEqual(A* mytuple.Idmatrix, A)

    
