###################################################################
#Purpose: This is the constants class, it creates all the contants#
#so they can be shared universally among other classes            #
###################################################################

#import dependencies
import pygame

#font constants
pygame.font.init()
ARIAL = pygame.font.SysFont("arial", 10)
FONT = pygame.font.Font('font.ttf', 23)
FONT_BIG = pygame.font.Font('font.ttf', 40)
FONT_BIGGEST = pygame.font.Font('font.ttf', 100)

#sound constants
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(True) #plays background music
SOUND_SHOT = pygame.mixer.Sound(file="shot.ogg")
SOUND_ROCKET = pygame.mixer.Sound(file="rocket.ogg")
SOUND_POINT = pygame.mixer.Sound(file="point.ogg")
SOUND_GAMEOVER = pygame.mixer.Sound(file="gameover.ogg")
SOUND_BUTTON = pygame.mixer.Sound(file="button.ogg")

#creates universal clock object
CLOCK=pygame.time.Clock()

#constants to tell rendering how much to scale up the spheres
SCALEUP = 50

#color constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
COLOR_BG = BLACK
COLOR_TEXT = WHITE

#game constants
INITIAL_SPHERES = 30
TIME_LIMIT = 120
SPHERES_LIMIT = 100
MAX=30

#screen constants
SIZE = [720, 720]
ORIGIN = [SIZE[0]/2,SIZE[1]/2]
