###################################################################
#Purpose: This is the RenderUtils class, it handles all of        #
#the rendering processes: Buttons, Fonts... Along with other game #
#mechanics such as keeping scores                                 #
###################################################################

#imports for dependencies
import pygame
import numpy as np
from math import *
from CONSTANTS import *
import player
import Sphere
from ScreenType import *
from random import randint

#initializes game
def initGame():
    #resets player score, position, aim, and rotations
    player.score=0
    player.x=0
    player.y=0
    player.z=0
    player.yaw=0
    player.pitch=0
    player.roll=0
    player.fromScreenD=3.5
    #resets timer
    if(player.mode=="timed"):
        player.timePassed = 0
    #resets spheres array
    Sphere.spheres=[]
    #Generate 30 spheres in the beginning of the game
    for i in range(0,INITIAL_SPHERES):  
        Sphere.Sphere([randint(-MAX,MAX), randint(-MAX,MAX), randint(-MAX,MAX)])

#The Button class
class Button():
    #constructor
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.buColor = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #Draws the button
    def draw(self,screen,clicking):
        #draws background of button on to the screen
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        #draws text onto the screen
        if self.text != '':
            text = FONT.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        #handles button mechanics
        if(self.isMouseOver() and clicking):
            #plays the button click sound
            SOUND_BUTTON.play()

            #handles button mechanics for INTRO screen
            if(player.screenType == ScreenType.INTRO):
                #The following checks which button is pressed and does the corresponding actions: Pretty self-explanatory
                if(self.text=="Timed Mode"):
                    player.mode = "timed"
                    initGame()
                    player.screenType = ScreenType.GAME
                elif(self.text=="Hardcore Mode"):
                    player.mode = "hardcore"
                    initGame()
                    player.screenType = ScreenType.GAME
                elif(self.text=="Rules"):
                    player.screenType = ScreenType.RULES
                elif(self.text=="Quit"):
                    pygame.quit()
                    exit()
                    
            #handles button mechanics for GAMEOVER screen
            elif(player.screenType == ScreenType.GAMEOVER or player.screenType == ScreenType.RULES):
                #When "Back" is pressed, set screen to INTRO
                if(self.text=="Back"):
                    player.screenType = ScreenType.INTRO

    #Checks if mouse is over button
    def isMouseOver(self):
        #Pos is the mouse position
        pos=pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                #Set hover color
                self.color=(100,100,100)
                return True
        #remove hover color
        self.color=self.buColor
        return False

#generates random color and returns it
def randomColor():
    return (randint(0,255), randint(0,255), randint(0,255))

#inits pygame & screen
pygame.init()
screen = pygame.display.set_mode(SIZE)

#load images
crosshair = pygame.image.load("crosshair.png")
tcrosshair = pygame.image.load("crosshair-target.png")
gameover = pygame.image.load("gameover.jpg")
rulesBG = pygame.image.load("rulesBG.png")

#Creates Buttons
startY=200
Button_Timed_Mode = Button(randomColor(), SIZE[0]/2-150, startY, 300, 100, text="Timed Mode")
Button_Hardcore_Mode = Button(randomColor(), SIZE[0]/2-150, startY+130, 300, 100, text="Hardcore Mode")
Button_Rules = Button(WHITE, SIZE[0]/2-150, startY+260, 300,100, text="Rules")
Button_Quit = Button(RED, SIZE[0]/2-150, startY+390, 300, 100, text="Quit")
Button_Back = Button(randomColor(), SIZE[0]/2-150, startY+390, 300, 100, text="Back")

#Draw Screen for Each ScreenType
#Draws Introduction Screen
def drawIntro(clicking, changeTitleColor):
    #creates global titleColor variable so it doesn't reset every time function is called
    global titleColor
    #draws background
    screen.fill(COLOR_BG)
    #every 2 seconds the changeTitleColor variable is set true,
    #and titleColor gets randomized
    if(changeTitleColor):
        titleColor = randomColor()
    try:
        #renders the title text
        screen.blit(FONT_BIGGEST.render('3D', False, titleColor),(260,20))
        screen.blit(FONT_BIG.render('SPACE SHOOTER', False, titleColor),(120,120))
    except NameError:
        #FIXED ERROR: fixes the error when titleColor is not initialized 
        titleColor = randomColor()
    #Draws buttons
    Button_Timed_Mode.draw(screen, clicking)
    Button_Hardcore_Mode.draw(screen, clicking)
    Button_Rules.draw(screen, clicking)
    Button_Quit.draw(screen, clicking)

#draws GameOver screen
def drawGameOver(clicking):
    #draws background
    screen.fill(COLOR_BG)
    #draws gameover image
    screen.blit(gameover, (SIZE[0]/2-315,SIZE[0]/2-340))
    #draws score text
    screen.blit(FONT_BIG.render('Your Score was: '+str(player.score), False, COLOR_TEXT), (100,50))
    #draws back button
    Button_Back.draw(screen, clicking)

#Draws Rules screen
def drawRules(clicking):
    #draws background
    screen.fill(COLOR_BG)
    #draws Rules image
    screen.blit(rulesBG, (0,-15))
    #draws back button
    Button_Back.draw(screen, clicking)

#Draws Game Screen
def drawGame(shooting, dt):
    #draws background
    screen.fill(COLOR_BG)
    #draws all the spheres
    Sphere.drawAll()
    #draws crosshair
    drawCrossHair(shooting)
    #draws player score
    screen.blit(FONT.render('Score: '+str(player.score) + " (Highest: "+str(player.highScore)+")", False, COLOR_TEXT), (10,0))
    if(player.mode =="timed"):
        #updates timer
        player.timePassed+=dt
        #draws time left text
        screen.blit(FONT.render('Time left: '+str(TIME_LIMIT-player.timePassed//1000)+"s", False, COLOR_TEXT), (10,50))
        #game mechanics: if time goes beyond time limit sets screen to gameover
        if(TIME_LIMIT-player.timePassed//1000<0):
            player.screenType = ScreenType.GAMEOVER
            SOUND_GAMEOVER.play()
    elif(player.mode == "hardcore"):
        #draws # of spheres text
        screen.blit(FONT.render('# of Spheres: '+str(len(Sphere.getSpheres()))+ " (Max: 35)", False, COLOR_TEXT), (10,50))
        #game mechanics: if spheres goes beyond limit set screen to gaveover
        if(len(Sphere.getSpheres())>SPHERES_LIMIT):
            player.screenType = ScreenType.GAMEOVER
            SOUND_GAMEOVER.play()

#Technical Functions
def drawPoint(coords, s, color):
    #to make the program more efficient, it will only draw point
    #if it's in the screen
    if(inScreen(coords, s)):
        #draws point
        pygame.draw.circle(screen, color, [int(coords[0]), int(coords[1])], int(s))

def drawCrossHair(shooting):
    #to make the code easier to read, I've created center_x and y variables
    center_x=SIZE[0]/2
    center_y=SIZE[0]/2
    #sets image variable to crosshair image
    image = crosshair
    #fetches data from sphere to see if center of screen/crosshair is in a sphere
    insideData=Sphere.isInAnySphere(center_x,center_y)
    #sets default cross hair color to green
    color = GREEN
    #if crosshair is inside a sphere: successful target
    if(insideData[0]):
        #sets image to targeted crosshair
        image = tcrosshair
        #sets color to red
        color = RED
        #if player is shooting/press spacebbar
        if(shooting):
            #deletes the sphere from array
            insideData[1].delete()
            #increment player score
            player.score +=1
            #play successful point sound
            SOUND_POINT.play()
            #updates highscore & writes it to file
            if(player.highScore < player.score):
                player.highScore=player.score
                player.saveHighScore()
                
    #draws the crosshair: self-explanatory
    pygame.draw.line(screen, color, [center_x-30, center_y-3], [center_x+30, center_y-3], 3)
    pygame.draw.line(screen, color, [center_x-3, center_y-30], [center_x-3, center_y+30], 3)
    screen.blit(image, (SIZE[0]/2-160,SIZE[0]/2-120))

#in screen function, pretty self-explanatory
def inScreen(point, rad):
    #checks if input is a valid x,y array
    if len(point)!=2:
        return False
    #checks if point is in screen
    elif point[0]<=SIZE[0]+rad and point[1]<=SIZE[1]+rad and point[0]>=0-rad and point[1]>=0-rad:
        return True
    else:
        return False
