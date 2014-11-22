import pygame
import math
import random
import time
from pygame.locals import*
from item import *
from block import *
from combat import*
from codex import*

offset_top=1
offset_bottom=0
offset_left=5
offset_right=-5  # panta peftei me thn deksia meria pano sto wall logo tou image.transform.flip ara left= -right
step = 3

def handle_event(event,key,obj,block_group,player_group,walls,animation_counter,animation_interval,camera,monster_group,item_group,collidables,screen,window):
    dx=0
    dy=0
##    if event.type == KEYDOWN:
##        if event.key == K_DOWN:
##            dy=1
##        elif event.key == K_UP:
##            dy=-1
##        elif event.key == K_LEFT :
##            dx=-1
##        elif event.key == K_RIGHT:
##            dx=1
    if key[pygame.K_0]:
        pygame.display.set_mode((800,600))
    if key[pygame.K_9]:
        pygame.display.set_mode((800,600),FULLSCREEN)
##    if key[pygame.K_e]:   # TO XO STO AUTO-PICKUP TORA
##        for item in item_group:  
##            item.pick_up(item,obj,item_group)
    if key[pygame.K_1]:
        obj.set_ammoType(1)
        obj.set_Damages()
    if key[pygame.K_2]:
        obj.set_ammoType(2)
        obj.set_Damages()
    if key [pygame.K_3]:
        obj.set_ammoType(3)
        obj.set_Damages()
    if key[pygame.K_a]:
        obj.move(-step,0,collidables,walls,camera)
        dx=-1
        #camera[0]-=step
        #obj.set_direction('left')
        if animation_counter >= animation_interval/2:
        #print animation_counter
            obj.image=pygame.image.load('images/knight_right_2.png')
            obj.image=pygame.transform.flip(obj.image,True,False)
            obj.image.set_colorkey((255,255,255))
        else:
        #print animation_counter
            obj.image=pygame.image.load('images/knight_right_1.png')
            obj.image=pygame.transform.flip(obj.image,True,False)
            obj.image.set_colorkey((255,255,255))


    if key[K_s]:
        obj.move(0,step,collidables,walls,camera)
        dy=1
        #camera[1]+=step
        if animation_counter >= animation_interval/2:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_center_2.png')
            obj.image.set_colorkey((255,255,255))
        else:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_center_3.png')
            obj.image.set_colorkey((255,255,255))
    if key[K_w]:
        obj.move(0,-step,collidables,walls,camera)
        dy=-1
        #camera[1]-=step
        if animation_counter >= animation_interval/2:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_upwards_2.png')
            obj.image.set_colorkey((255,255,255))
        else:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_upwards_3.png')
            obj.image.set_colorkey((255,255,255))
    #elif event.key == K_LEFT :

    if key[K_d]:
        obj.move(step,0,collidables,walls,camera)
        dx=1
        #camera[0]+=step
        if animation_counter >= animation_interval/2:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_right_2.png')
            obj.image.set_colorkey((255,255,255))
        else:
            #print animation_counter
            obj.image=pygame.image.load('images/knight_right_1.png')
            obj.image.set_colorkey((255,255,255))
        #obj.set_direction('right')
            
    if key[K_i]:
        #window.fill((0,0,0))
        codexViewer(1,screen,window)




    if key[K_SPACE] :
        if animation_counter<=animation_interval/2:
            combat_player_attack(obj,monster_group,player_group,walls)
            if dx>0:
                obj.image=pygame.image.load('images/knight_right_2 _attack.png')
                obj.image.set_colorkey((255,255,255))
            if dx<0:
                obj.image=pygame.image.load('images/knight_right_2 _attack.png')
                obj.image=pygame.transform.flip(obj.image,True,False)
                obj.image.set_colorkey((255,255,255))
            if dy<0:
                obj.image=pygame.image.load('images/knight_upwards_attack.png')
                obj.image.set_colorkey((255,255,255))
            if dy>0:
                obj.image=pygame.image.load('images/knight_center_attack.png')
                obj.image.set_colorkey((255,255,255))



            
def collision(walls,obj,dx,dy,camera,monster_group,player_group):
    for wall in walls:
         step=3
         if pygame.sprite.collide_mask(obj,wall)!= None:
         #gia to mask anti gia obj.rect.right = wall .rect.left kalitera na to setaro se (objblabla=wall.rect.left-x) opou x einai h apostash ths figouras apo ta plagia
         #boundaries tou rectangle pou orizei. gia na to vro arkei na metriso apo to meros pou proeksexei perissotero sthn figoura(to xeri mallon)mexri to edge tou tetragonou
            if dx > 0: # Moving right; Hit the left side of the wall
                obj.move(-step,0)
                camera[0]-=step
            if dx < 0: # Moving left; Hit the right side of the wall
                obj.move(step,0)
                camera[0]+=step
            if dy > 0: # Moving down; Hit the top side of the wall
                obj.move(0,-step)
                camera[1]-=step
            if dy < 0: # Moving up; Hit the bottom side of the wall
                 obj.move(0,step)
                 camera[1]+=step
            # diagonals
##            if dy>0 and dx>0:
##                obj.move(-step,-step)
##                camera[0]-=step
##                camera[1]-=step
##            if dy<0 and dx>0:
##                obj.move(-step,step)
##                camera[0]-=step
##                camera[1]+=step
##            if dy<0 and dx<0:
##                obj.move(step,step)
##                camera[0]+=step
##                camera[1]+=step
##            if dy>0 and dx<0:
##                obj.move(step,-step)
##                camera[0]+=step
##                camera[1]-=step
