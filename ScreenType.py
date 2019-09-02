###################################################################
#Purpose: This is the ScreenType class, it is an ENUM class used  #
#to create a "ScreenType" structure. This is useful because       #
#instead of using numbers when setting and checking screentypes,  #
#you can use english words which makes the code more readable     #
###################################################################

#import dependencies
from enum import Enum

#creates the 4 screentypes: intro, rules, game, gameover, pretty self-explanatory
class ScreenType(Enum):
    INTRO=1
    RULES=2
    GAME=3
    GAMEOVER=4
