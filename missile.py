import pygame
import math
import random
import time
from pygame.locals import*
from particles import*




class Missile(pygame.sprite.Sprite):
    def __init__(self, imagefile, start_point, end_point,window,walls,monsters,number_of_particles,my_particles,damage,pie):
        pygame.sprite.Sprite.__init__(self)
        self.screen = window
        self.area = self.screen.get_rect()
        self.walls=walls
        self.monsters=monsters
        self.number_of_particles=number_of_particles
        self.my_particles=my_particles
        self.damage=damage
    
        # Set up the sprite's initial image
        self.image = pygame.image.load(imagefile).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = start_point

        self.target = end_point # GIA TO PI ITEM APLA self.target = start point, self.start_point = end_point ( apla swap ta end_point kai start_point)
        self.start_point = start_point
        if(pie == True):
            self.target = start_point
            self.start_point = end_point
        self.target_hit = False
        self.speed_constant = .05
        
    def update(self,walls):
        speed = 5 #[self.speed_constant*(self.target[0] - self.rect.centerx),self.speed_constant*(self.target[1] - self.rect.centery)]
        if self.target_hit != True:  # keep going after the end point is hit
            #oso poio makria kaneis click toso poio grigora paei.(tha einai bow ara ama varas konta einai san na min vazeis pollh dinami)
            #self.target_hit = True
            speed = [self.speed_constant*(self.target[0] - self.start_point[0]),self.speed_constant*(self.target[1] - self.start_point[1])]
        self.rect.move_ip(speed)
        if self.rect.left < 0 or self.rect.right > self.area.width or self.rect.top < 0 or self.rect.bottom > self.area.height:
            # the missile went off the screen without hitting anything
            self.kill()
        if self.rect.collidelist(walls) != -1 :
            self.kill()
##        for wall in self.walls:
##            if pygame.sprite.collide_mask(self,wall)!= None:
##                self.target_hit=True
##                coord=self.rect.center
##                #particle(coord)
##                #particle_create(coord,self.number_of_particles,self.my_particles,self.screen)

        for monster in self.monsters:
            if pygame.sprite.collide_mask(self,monster)!= None:
                if(monster.twin == 1 or monster.twin == 2):
                    monster.death_twins(self.monsters,int(self.damage),walls)
                else:
                    monster.death(self.monsters,int(self.damage),walls)
                self.target_hit=True
                coord=self.rect.center
                #particle(coord)
                #particle_create(coord,self.number_of_particles,self.my_particles,self.screen)    
        if self.target_hit==True:
            self.kill()
