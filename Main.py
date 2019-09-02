###################################################################
#Purpose: This is the MAIN class of the "3D Space Shooter" Game.  #
#This class handles the main loop, events, and sphere generation. #
#Other functions has been separated into other classes for the    #
#sake of simplifying the code and making it easier to read.       #
###################################################################

#imports for dependencies
import numpy as np
import pygame
from Sphere import *
import RenderUtils
import player
from random import randint
from ScreenType import *

#Initializing Variables
keyPressed=[]
time_elasped=0
speed = 0
yawSpeed = 0
pitchSpeed = 0
rollSpeed = 0

#Main Game Loop
while True:
    #Initializing Boolean Variables at the beginning of each frame
    shooting=False
    clicking=False

    #Game Event Loop(self-explanatary)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                #sets clicking to True after player clicks mouse button
                #(It's MOUSEBUTTONUP since a click is only fully registered after the user lifts his mouse button)
                clicking=True
            #checks to see if the player's screenType is GAME AND if event type is keydown or keyup
            #reason behind this is you only want the program to handle keyboard inputs when a player is in a game
            elif player.screenType == ScreenType.GAME and (event.type in (pygame.KEYDOWN, pygame.KEYUP)):
                # gets the key name
                key_name = pygame.key.name(event.key)
                # converts to uppercase the key name
                key_name = key_name.upper()

                # if any key is pressed
                if event.type == pygame.KEYDOWN:
                    #Adds the key name to keyPressed
                    keyPressed.append(key_name)
                    if key_name == "SPACE":
                        #Sets shooting = True and plays shoot sound when spacebar is pressed
                        SOUND_SHOT.play()
                        shooting = True
                # if any key is released
                elif event.type == pygame.KEYUP:
                    #FIXED BUG: if statement is used to fix the error in the rare case the key_name is not already in keyPressed
                    if(key_name in keyPressed):
                        #removes the key name to keyPressed
                        keyPressed.remove(key_name)
                    #stops playing rocket sound
                    SOUND_ROCKET.stop()
    #Here's where all the code for the INTRO screen lies
    if (player.screenType == ScreenType.INTRO):
        #initialize changeTitleColor and Clock
        changeTitleColor=False
        CLOCK = pygame.time.Clock()
        #timer to change title color
        if(pygame.time.get_ticks()%2000==0):
            changeTitleColor = True
        #draw intro screen
        RenderUtils.drawIntro(clicking, changeTitleColor)
        #FIXED BUG: resets keyPressed because sometimes pygame never calls the keyUp event,
        #leading the program to think the key is pressed when it isn't.
        keyPressed=[]
        #FIXED BUG: speed values didn't reset for new game
        yawSpeed = 0
        pitchSpeed = 0
        rollSpeed = 0
        speed = 0
    #Here's where all the code for the GAME screen lies
    elif(player.screenType == ScreenType.GAME):
        player.z+=speed
        #Matrix Transformations(3D rotations)
        transformAll(yawSpeed,"Y")
        transformAll(pitchSpeed,"X")
        transformAll(rollSpeed,"Z")
        sortSpheres()
        for key in keyPressed:
            #Move Forward
            if key == "F"or key == "UP":
                speed+=0.0001
                SOUND_ROCKET.play(-1)
            #Move Backward
            elif key == "G" or key == "DOWN":
                speed-=0.0001
                SOUND_ROCKET.play(-1)
            #Aim Up
            elif key == "W":
                pitchSpeed+=0.00004
            #Aim Down
            elif key == "S":
                pitchSpeed-=0.00004
            #Aim Left
            elif key == "A":
                yawSpeed+=0.00004
            #Aim Right
            elif key == "D":
                yawSpeed-=0.00004
            #rotates vision left
            elif key == "Q":
                rollSpeed += 0.00004
            #rotates vision right
            elif key == "E":
                rollSpeed -= 0.00004
            #aim harder/decrease FOV
            elif key == "[+]":
                player.fromScreenD+=0.005
            #aim less/increase FOV
            elif key == "[-]":
                #FIXED ERROR: screen cannot be behind player
                if(player.fromScreenD>0.01):
                    player.fromScreenD-=0.005
        #finds the difference to the previous call in ms
        dt = CLOCK.tick()
        #adds difference to time_elapsed(timer)
        time_elasped += dt
        #Sphere Generation(2 new spheres every second)
        if time_elasped > 2000:
            Sphere([randint(-MAX,MAX), randint(-MAX,MAX), randint(-MAX,MAX)])
            time_elasped = 0
        #draws game screen
        RenderUtils.drawGame(shooting, dt)
    #Here's where all the code for the GAMEOVER screen lies
    elif(player.screenType == ScreenType.GAMEOVER):
        #draws gameover screen
        RenderUtils.drawGameOver(clicking)
        #FIXED BUG: sometimes the rocket sound would play after the game is over, this is to prevent that
        SOUND_ROCKET.stop()

        #FIXED BUG: resets keyPressed because sometimes pygame never calls the keyUp event,
        #leading the program to think the key is pressed when it isn't.
        keyPressed=[]
    #Here's where all the code for the RULES screen lies
    elif(player.screenType == ScreenType.RULES):
        RenderUtils.drawRules(clicking)
        #FIXED BUG: resets keyPressed because sometimes pygame never calls the keyUp event,
        #leading the program to think the key is pressed when it isn't.
        keyPressed=[]
    #updates screen
    pygame.display.flip()
#quits mixer and pygame
pygame.mixer.quit()
pygame.quit()


