import pygame
import math
import random
import time
from main import ask,display_box


def ShopGenerator(s):
    basicfont = pygame.font.SysFont(None, 20)
    #TODO: find out how to newline
    #TODO: read the stories from a file
    story ="Answer this simple riddle traveler and the reward shall be yours!"
    story2= "A fair princess sends you to gather flowers for her bouquet.Her request was..."
    story3 ="All but two to be roses, all but two to be tulips and all but two to be daises. How many flowers should you gather traveler?"
    textshop = basicfont.render(story, True, (255, 0, 0))
    textshop2 = basicfont.render(story2,True,(255,0,0))
    textshop3 = basicfont.render(story3,True,(255,0,0))
    s.fill((0,0,0))
    s.blit(textshop,(0,100))
    s.blit(textshop2,(0,120))
    s.blit(textshop3,(0,130))
    Myinput = ask(s, "Answer")
    if(Myinput == "3"):
        print "CORRECT"
