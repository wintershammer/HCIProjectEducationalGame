import pygame
import math
import random
import time


def ShopGenerator():
    choice = random.randint(0,3) #choice of problem framework!
    var1 = random.randint (0,10)
    var2 = random.randint (0,10)
    probText = "Exo {} mila kai troo ta {}".format(var1,var2)
    print probText
    apantish = raw_input("APANTISH:")
    if apantish == str(var1-var2):
        print "YOU WIN! :D"
    else:
        print "YOU LOOOOOOSE!"

ShopGenerator()
