import pygame
import math
import random
import time
from questioner import *


def codexViewer(page,s,window):
    page = int(ask(s, "Page: "))
    if(page == 1):
        shopStory = pygame.image.load("images/codex1.png")
    elif(page == 2):
        shopStory = pygame.image.load("images/codex2.png")
    elif(page == 3):
        shopStory = pygame.image.load("images/codex3.png")
    elif(page == 4):
        shopStory = pygame.image.load("images/codex4.png")
    window.fill((0,0,0))
    s.fill((0,0,0))
    s.blit(shopStory,(0,0))
    page = ask(s, "Push Any Button to Exit: ")
