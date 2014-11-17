import pygame
import math
import random
from monster import*
import time
from block import *
from pygame.locals import*
from particles import *
from missile import *



def combat(player,monster_group,player_group,my_particles,combat_counter):
    for monster in monster_group:
        if monster.get_attack_mode() == 1:
            if monster.distance_to(player) < monster.get_range():
                if pygame.sprite.collide_mask(player,monster)!= None:
                    player.death(player_group,monster.get_damage())
        for missile in my_particles:
            if pygame.sprite.collide_mask(missile,monster) != None:
                monster.death(monster_group,missile.get_damage())
                missile.set_target_hit=True
                coord=missile.rect.center
                particle_create(coord,missile.number_of_particles,missile.my_particles,missile.screen)
                missile.kill()

def combat_player_attack(player,monster_group,player_group,walls):
    for monster in monster_group:
        if player.weapon==0:
            if monster.distance_to(player)<=40:
                if(monster.twin == 1 or monster.twin == 2):
                    monster.death_twins(monster_group,5,walls)
                else:
                    monster.death(monster_group,5,walls)
