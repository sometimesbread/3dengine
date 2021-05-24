from pygame import *
import classes3d
from classes3d import vec3
import math
from copy import deepcopy
import time
from math import cos, sin

#whoever is reading this (you are probably in my class if you are), thanks. sorry that the code
#is not very clean, i was doing this as fast as i could and im not TOO experienced with Python,
#and Python has some limitations when it comes to strict type casting.

#also, this code was actually from a tutorial from OneLoneCoder (OLC), and i just translated it to Python just
#to make it easier to understand (and also because C++ does not want to work on my computer).

#OLC's code from which i stol- i mean, adapted: https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_olcEngine3D_Part1.cpp

fpsCap = 60.0

currentTime = 0.0
previousTime = 0.0
deltaTime = 0.0

fTheta = 0.0

#tommy
init()

screenRes = classes3d.vec2()
#screenRes.x = 256
#screenRes.y = 210
screenRes.x = 512
screenRes.y = 420

#cube mesh

#south
cubeMesh = classes3d.mesh()
cubeMesh.m.append([[0.0, 0.0, 0.0], [0.0,1.0,0.0], [1.0, 1.0, 0.0]])
cubeMesh.m.append([[0.0 ,0.0 ,0.0],[1.0, 1.0, 0.0],[1.0, 0.0, 0.0]])

#east
cubeMesh.m.append([[1.0, 0.0, 0.0],[1.0, 1.0, 0.0],[1.0, 1.0, 1.0]])
cubeMesh.m.append([[1.0, 0.0, 0.0],[1.0, 1.0, 1.0],[1.0, 0.0, 1.0]])

#north
cubeMesh.m.append([[1.0, 0.0, 1.0],[1.0, 1.0, 1.0],[0.0, 1.0, 1.0]])
cubeMesh.m.append([[1.0, 0.0, 1.0],[0.0, 1.0, 1.0],[0.0, 0.0, 1.0]])

#west
cubeMesh.m.append([[0.0, 0.0, 1.0],[0.0, 1.0, 1.0],[0.0, 1.0, 0.0]])
cubeMesh.m.append([[0.0, 0.0, 1.0],[0.0, 1.0, 0.0],[0.0, 0.0, 0.0]])

#top
cubeMesh.m.append([[0.0, 1.0, 0.0],[0.0, 1.0, 1.0],[1.0, 1.0, 1.0]])
cubeMesh.m.append([[0.0, 1.0, 0.0],[1.0, 1.0, 1.0],[1.0, 1.0, 0.0]])

#bottom
cubeMesh.m.append([[1.0, 0.0, 1.0],[0.0, 0.0, 1.0],[0.0, 0.0, 0.0]])
cubeMesh.m.append([[1.0, 0.0, 1.0],[0.0, 0.0, 0.0],[1.0, 0.0, 0.0]])

#Matrix Multiplication
def MatrixVListMultiplication(point, m4):
    output = classes3d.vec3()
    output.x = (point[0] * m4.m[0][0]) + (point[1] * m4.m[1][0]) + (point[2] * m4.m[2][0]) + m4.m[3][0]
    output.y = (point[0] * m4.m[0][1]) + (point[1] * m4.m[1][1]) + (point[2] * m4.m[2][1]) + m4.m[3][1]
    output.z = (point[0] * m4.m[0][2]) + (point[1] * m4.m[1][2]) + (point[2] * m4.m[2][2]) + m4.m[3][2]
    w = point[0] * m4.m[0][3] + point[1] * m4.m[1][3] + point[2] * m4.m[2][3] + m4.m[3][3]

    if(w != 0.0):
        output.x/=w;output.y/=w;output.z/=w
    return output

def MatrixVector3Multiplication(point, m4):
    output = classes3d.vec3()
    output.x = (point.x * m4.m[0][0]) + (point.y * m4.m[1][0]) + (point.z * m4.m[2][0]) + m4.m[3][0]
    output.y = (point.x * m4.m[0][1]) + (point.y * m4.m[1][1]) + (point.z * m4.m[2][1]) + m4.m[3][1]
    output.z = (point.x * m4.m[0][2]) + (point.y * m4.m[1][2]) + (point.z * m4.m[2][2]) + m4.m[3][2]
    w = point.x * m4.m[0][3] + point.y * m4.m[1][3] + point.z * m4.m[2][3] + m4.m[3][3]

    if(w != 0.0):
        output.x/=w;output.y/=w;output.z/=w
    return output

def drawTriangle(x1, y1, x2, y2, x3, y3, r, g, b):
    draw.line(screen, (r,g,b), (x1,y1), (x2, y2))
    draw.line(screen, (r,g,b), (x2,y2), (x3,y3))
    draw.line(screen, (r,g,b), (x3, y3), (x1,y1))

#Projection Matrix

matProj = classes3d.matrix4x4() 

nearClip = 0.1
farClip = 1000.0
fov = 90.0
aspectRatio = 256/210
fovRad = 1.0/math.tan(fov * 0.5 / 180.0 * math.pi)

matProj.m[0][0] = aspectRatio * fovRad
matProj.m[1][1] = fovRad
matProj.m[2][2] = farClip / (farClip - nearClip)
matProj.m[3][2] = (-farClip * nearClip) / (farClip - nearClip)
matProj.m[2][3] = 1.0   
matProj.m[3][3] = 0.0

print(matProj.m)

#print(1.0 / math.tan(fov * 0.5 / 180.0 * 3.14159))

screen = display.set_mode((screenRes.x, screenRes.y))
display.set_caption("Genius Hour 3D Demo")
display.set_icon(image.load(r'C:\Users\Airer Undrscr Enythy\Desktop\[\genius hour\2d\icon.png'))
windowrun = True
while windowrun:
    for i in event.get():
        if i.type == QUIT:
            windowrun = False

    #calculate deltatime
    currentTime = time.time()
    deltaTime = currentTime - previousTime
    previousTime = time.time()

    #calculate fps to tenth place
    fps = 1/deltaTime
    fpsRounded = fps.__round__()

    display.set_caption("Genius Hour 3D Demo " + "FPS:" + str(fpsRounded))

    #clear screen
    screen.fill((0,0,0))


    #rotation matricies and elapsed time
    fTheta += 1.0 * deltaTime
    #draw triangles
    
    for tri in cubeMesh.m:
        triProjected = classes3d.triangle()
        triTranslated = classes3d.triangle()

        triTranslated = deepcopy(tri)
        triTranslated[0][0] -= 0.5
        triTranslated[1][0] -= 0.5
        triTranslated[2][0] -= 0.5

        triTranslated[0][1] -= 0.5
        triTranslated[1][1] -= 0.5
        triTranslated[2][1] -= 0.5

        triTranslated[0][2] += 2.0
        triTranslated[1][2] += 2.0
        triTranslated[2][2] += 2.0

        triProjected.point1 = MatrixVListMultiplication(triTranslated[0], matProj)
        triProjected.point2 = MatrixVListMultiplication(triTranslated[1], matProj)
        triProjected.point3 = MatrixVListMultiplication(triTranslated[2], matProj)

		#scale into view
        triProjected.point1.x += 1.0; triProjected.point1.y += 1.0
        triProjected.point2.x += 1.0; triProjected.point2.y += 1.0
        triProjected.point3.x += 1.0; triProjected.point3.y += 1.0
        triProjected.point1.x *= 0.5 * screenRes.x
        triProjected.point1.y *= 0.5 * screenRes.y
        triProjected.point2.x *= 0.5 * screenRes.x
        triProjected.point2.y *= 0.5 * screenRes.y
        triProjected.point3.x *= 0.5 * screenRes.x
        triProjected.point3.y *= 0.5 * screenRes.y

		#draw it
        drawTriangle(triProjected.point1.x, triProjected.point1.y, triProjected.point2.x, triProjected.point2.y, triProjected.point3.x, triProjected.point3.y, 255, 255, 255)
         
        display.update()