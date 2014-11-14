import pygame
import math
import random
import time
from pygame.locals import*






class Block(pygame.sprite.Sprite):
    def __init__( self,color=(193,63,43),width = 32,height = 32):
        super(Block,self).__init__()
        self.image=pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.road=0;
        self.wall=0;
        self.life=0;
        self.owner=0;
        self.weapon=0;
        self.strength=0
        self.agility=0
        self.intelligence=0
        self.ammo1=10
        self.ammo2=6
        self.ammo3=2
        self.spldmg=0;
        self.ammoType=1
        self.ammoDmg1 = 5
        self.ammoDmg2 = 10
        self.ammoDmg3 = 15
        self.powercharge = 10 #testing
        self.aoa = 0 #armor of absolute
        
    def equip_item(self,effect_type,effect_value):
        if effect_type == 1:
            self.life += effect_value
        if effect_type == 2:
            self.ammo1 += effect_value
        if effect_type == 3:
            self.powercharge += effect_value #effect_value here is charges of I GOT THE POWAH scroll/spell!
        if effect_type == 4: # Armor of absolute
            self.aoa = 1
            
    def increment_powercharge(self,value):
        self.powercharge += value

    def get_powercharge(self):
        return self.powercharge

    def set_owner(self,owner):
        self.owner=owner
    def set_life(self,hp):
        self.life=hp;
    def set_position(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def move(self,dx,dy,collidables,walls,camera):
        if dx > 0: # Moving right; Hit the left side of the wall
            if collidables[(self.rect.center[0]+dx+16)/32][(self.rect.center[1]+dy)/32] == False:
                self.rect.x+=dx
                self.rect.y+=dy
                camera[0]+=int(math.fabs(dx))
        if dx < 0: # Moving left; Hit the right side of the wall
            if collidables[(self.rect.center[0]+dx-16)/32][(self.rect.center[1]+dy)/32] == False:
                self.rect.x+=dx
                self.rect.y+=dy
                camera[0]-=int(math.fabs(dx))
        if dy > 0: # Moving down; Hit the top side of the wall
            if collidables[(self.rect.center[0]+dx)/32][(self.rect.center[1]+16+dy)/32] == False:
                self.rect.x+=dx
                self.rect.y+=dy
                camera[1]+=int(math.fabs(dy))
        if dy < 0: # Moving up; Hit the bottom side of the wall
            if collidables[(self.rect.center[0]+dx)/32][(self.rect.center[1]-16+dy)/32] == False:
                self.rect.x+=dx
                self.rect.y+=dy
                camera[1]-=int (math.fabs(dy))


    #def set_spldmg(self,value):
     #   self.spldmg = value
        
    def get_spldmg(self):
        return self.spldmg


    def get_ammo(self):
        if self.ammoType == 1:
            return self.ammo1
        elif self.ammoType == 2:
            return self.ammo2
        else:
            return self.ammo3

    def set_ammo(self,ammoType,value):
        if ammoType == 1:
            self.ammo1 = value
        elif ammoType == 2:
            self.ammo2 = value
        else:
            self.ammo3 = value


    def set_ammoType(self,value):
        self.ammoType = value
    def get_ammoType(self):
        return self.ammoType
    def set_Damages(self):
        if self.ammoType == 1:
            self.spldmg = self.ammoDmg1
        elif self.ammoType == 2:
            self.spldmg = self.ammoDmg2
        else:
            self.spldmg == self.ammoDmg3

    def set_ammoDmg(self,ammoType,value):
        if ammoType == 1:
            self.ammoDamage1 = value
        elif ammoType == 2:
            self.ammoDamage2 = value
        else:
            self.ammoDamage3 = value
            
    def increment_ammo(self,value):
        if self.ammoType == 1:
            self.ammo1 += value
        elif self.ammoType == 2:
            self.ammo2 += value
        else:
            self.ammo3 += value
    def death(self,player_group,damage):
        self.life -= damage
        if self.life <= 0 and self.aoa <= 0:
            player_group.remove(self.owner)
        elif self.life <= 0 and self.aoa >= 1:
            self.life += damage
            self.aoa -= 1

    def set_image(self,filename=None):
        if(filename!=None):
            self.image=pygame.image.load(filename).convert_alpha()
            #self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image,127)
    def set_direction(self,direction):
        if direction == 'left':
            a_block.image=pygame.transform.flip(a_block.image,True,False)
        if direction == 'right':
            a_block.image=pygame.transform.flip(a_block.image,True,False)
