###################################################################
#Purpose: This is the player class, it handles all of the player  #
#variables to be universally shared among other classes           #
###################################################################

#import dependencies
from ScreenType import *

#creates player variables: self-explanatory
x,y,z=0,0,0
yaw,pitch,roll=0,0,0
fromScreenD = 3.5
score=0

#initializes highscore variable from file
highScoreFile = open("highScore.txt", "r")
highScore=int(highScoreFile.read())
highScoreFile.close()

#initalizes screenType to INTRO screen
screenType = ScreenType.INTRO

#game modes: timed or hardcore, default: Timed
mode = "timed"
#initializes time passed to 0
timePassed = 0

#getters and setters
#position
def getPos():
    return [x,y,z]
def setPos(pos):
    global x,y,z
    x,y,z=pos
#camera angles
def getCam():
    return [yaw,pitch,roll]
def setCam(cam):
    global yaw,pitch,roll
    yaw,pitch,roll=cam
#highscore
def getHighScore():
    return highScore
def saveHighScore():
    #saves high score to file
    highScoreFile = open("highScore.txt", "w")
    highScoreFile.write(str(highScore))
    highScoreFile.close()
