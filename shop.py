import pygame
import math
import random
import time
from main import ask,display_box


def ShopGenerator(s):
    basicfont = pygame.font.SysFont(None, 20)
    story = "STORY GOES HERE"
    textshop = basicfont.render(story, True, (255, 0, 0))
    s.fill((0,0,0))
    s.blit(textshop,(100,100))
    input = ask(s, "Answer")
    if(input == "solution"):
        print "CORRECT"
