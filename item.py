import pygame
import math
import random
import time
from pygame.locals import*






class Item(pygame.sprite.Sprite):
    def __init__( self,color=(193,63,43),width = 32,height = 32):
        super(Item,self).__init__()
        self.image=pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.effect_type=0 # 1 for strength / 2 for intelligence etc
        self.effect_value=0 # ie: self effect type = 1 / effect value =10 -> add +10 to strength
        
    def set_owner(self,owner):
        self.owner=owner
    def set_life(self,hp):
        self.life=hp;
    def set_position(self,x,y):
        self.rect.x=x
        self.rect.y=y
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    def set_image(self,filename=None):
        if(filename!=None):
            self.image=pygame.image.load(filename)
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image,127)

    def distance_to(self, other):
        #return the distance to another object
        dx = other.rect.x - self.rect.x
        dy = other.rect.y - self.rect.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def effects(self,effect_type,effect_value):
        self.effect_type=effect_type
        self.effect_value=effect_value
    def pick_up(self,item,player,item_group):
        if item.distance_to(player) < 40:
            item_group.remove(self.owner)
            player.equip_item(self.effect_type,self.effect_value)
