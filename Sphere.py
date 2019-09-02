###################################################################
#Purpose: This is the Sphere class. This handles the majority of  #
#the linear algebra math involved in 3D to 2D projection. It also #
#holds the blueprint for the sphere object which can be created   #
#multiple times.                                                  #
###################################################################

#import dependencies
from numpy import array
import player
import numpy as np
from math import *
from CONSTANTS import * 
import RenderUtils
#sets constant radius to 5
RADIUS = 5
#initializes spheres array
spheres = []
class Sphere():
    #constructor
    def __init__(self, coords=[0,0,0]):
        #sets object variables, pretty self-explanatory
        self.x=coords[0]
        self.y=coords[1]
        self.z=coords[2]
        self.color = RenderUtils.randomColor()
        #FIXED ERROR: sometimes this function is called
        #before the first spheres = [] line is called,
        #therefore in this case, you must create a global
        #spheres variable to prevent error
        global spheres
        #adds the created sphere into the array
        spheres.append(self)

    #gets coordinates for sphere
    def getCoords(self):
        return [self.x,self.y,self.z]

    #sets coordinates
    def setCoords(self, coords):
        self.x=coords[0]
        self.y=coords[1]
        self.z=coords[2]

    #get 3D distance from player to sphere
    def getDistance(self):
        playerPos = player.getPos()
        return ((self.x-playerPos[0])**2+(self.y-playerPos[1])**2+(self.z-playerPos[2])**2)**0.5

    #calculates Real Radius of sphere
    def getRealRadius(self):
        #uses linear algebra to figure out a 2D projected radius of sphere
        return RADIUS/max(0.0000000000001,self.getDistance())*player.fromScreenD*SCALEUP
                    #FIXED ERROR: ^This is to prevent divide by 0

    #Converts not only to 2D but also adds transformation and Cam angles
    def get2D(self):
        #creates a copy of coordinates and stores it in a temporary coordinate variable
        #You must do this since python passes lists by reference by default
        tC = np.copy(self.getCoords())
        x=tC[0]
        y=tC[1]
        z=tC[2]
        #Checks if sphere is behind to in front of player
        if((z-player.z)*100>player.fromScreenD):
            if(player.z-z==0):
                #FIXED ERROR: adds a small amt to prevent dividing by 0
                z+=0.00000001
            #Here's the linear algebra math for the 3D to 2D projection
            fx = (player.x-x)*(player.fromScreenD/(player.z-z))*SCALEUP
            fy = (player.y+y)*(player.fromScreenD/(player.z-z))*SCALEUP
            #returns point(adds origin to it to make it compatible with pygame's coordinate system)
            return np.array([ORIGIN[0]+fx,ORIGIN[1]-fy])
        #returns empty array(invalid 2d point) if sphere is behind player
        else:
            return []

    #TransformsPoints in 3D space
    def transformPoints(self, degree, fixedAxis):
        #creates a copy of coordinates and stores it in a temporary coordinate variable
        #You must do this since python passes lists by reference by default
        tC = np.array(np.copy(self.getCoords()),dtype=float)
        #initializes transformation matrix
        transformation = []

        #according to the fixedAxis, set transoformation matrix to the according linear algebra matrix
        if fixedAxis.upper() == "X":
            transformation = [[1,0,0],[0,cos(degree),sin(degree)],[0,-sin(degree),cos(degree)]]
        elif fixedAxis.upper() == "Y":
            transformation = [[cos(degree),0,sin(degree)],[0,1,0],[-sin(degree),0,cos(degree)]]
        elif fixedAxis.upper() == "Z":
            transformation = [[cos(degree),sin(degree),0],[-sin(degree),cos(degree),0],[0,0,1]]

        #Offets point by player position
        #this is done so rotation is done about the player position
        #instead of (0,0,0)
        tC[0]-=player.x
        tC[1]-=player.y
        tC[2]-=player.z

        #Takes the dot product of the transformation matrix with the point to rotate it
        tC = np.dot(transformation,tC)

        #Offets point back after the rotation
        tC[0]+=player.x
        tC[1]+=player.y
        tC[2]+=player.z
        #sets sphere coordinates to new coordinate
        self.setCoords(tC)

    #Draws sphere in 2D and acoording to it's real radius and color
    def drawSphere(self):
        RenderUtils.drawPoint(self.get2D(), self.getRealRadius(), self.color)

    #Checks if a coordinate is in the 2D projected version of sphere
    def isInSphere(self, x, y):
        #FIXED ERROR: checks if length is 2 incase self.get2D() returns an empty array
        if(len(self.get2D())!=2):
            return False
        #fetches center of sphere in 2D and real radius
        center_x=self.get2D()[0]
        center_y=self.get2D()[1]
        rad=self.getRealRadius()
        #Uses pythagorean theorum to check if point is instead projected sphere
        #This code is similar to sphere collisions except done with a point
        if((x-center_x)**2 + (y - center_y)**2 < rad**2):
            return True
        else:
            return False

    #Deletes sphere from the spheres array
    def delete(self):
        spheres.remove(self)

#returns all spheres in a single array
def getSpheres():
    return spheres

#transforms ALL spheres in the spheres array according to degree and axis
def transformAll(degree, fixedAxis):
    #loops through all spheres
    for i in getSpheres():
        i.transformPoints(degree, fixedAxis)

#draws ALL spheres
def drawAll():
    #loops through all spheres
    for i in getSpheres():
        i.drawSphere()

#Sorts the spheres from furtherest to nearest, method: Bubble Sort
def sortSpheres():
    numSpheres = len(spheres)
    #loops from 0 to numSpheres
    for i in range(numSpheres):
        #loops from 0 to numSpheres - i - 1(This is done so the "swap" happens from the "left side" and "right side". Search "Bubble Sort" on google for indepth explanation)
        for j in range(0, numSpheres-i-1):
            #if distance of first sphere is smaller than 2nd sphere, it gets swapped with it
            if spheres[i - 1].getDistance() < spheres[i].getDistance():
                #swaps first sphere's place in the array with 2nd
                spheres[i-1], spheres[i] = spheres[i], spheres[i - 1]

#checks if point is in ANY sphere
#returns the above value. If true, also returns the exact sphere object
def isInAnySphere(x,y):
    #loops through all spheres
    for i in getSpheres():
        if(i.isInSphere(x,y)):
            return [True, i]
    return [False]
