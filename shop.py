import pygame
import math
import random
import time
from questioner import ask


def ShopGenerator(s):
    shopStory = pygame.image.load("images/shop1.png")
    s.fill((0,0,0))
    s.blit(shopStory,(0,130))
    Myinput = ask(s, "Answer")
    if(Myinput == "3"):
        print "CORRECT"


