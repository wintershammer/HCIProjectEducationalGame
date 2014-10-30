import pygame
import math
import time
from random import randrange
from block import *
from item import*
from monster import*
from particles import *
from missile import *
from eventhandler import *
from pygame.locals import*
from level_generator import *
from combat import*
# isos na boro na xrisomopoiiso kai alla mikra kommatia tou background gia na dimiourgiso enan kiklo h enan stauro-like field of view.kinda like using rectangles/pixels to create a circle
#ean kanei collide kapou o pexths h kamera sinexizei kai o pextis vgenei ektos view. ara oso kai na ton kinigas me thn kamera
# o pextis einai panta ligo poio pano
# isos na mporo na kano blit me blend gri gia oti den exo kanei discover akoma kai "anti-gri" gia oti exo kanei ( antigri + gri = regular xroma?!?)
# KSEXNA TA WALK INTERVALS.BOTH YOU AND ENEMIES VALTA NA PERPATANE STHN IDIA TAXITITA( PEKSE ME TO FPS GIA SMOOTHER /SLOWER MOVEMENT) KAI VALE KNOCKBACK STIS EPITHESEIS
# GIA NA MIN KANOUNE KEEP UP WITH YOU OI ENEMIES
animation_interval=20
particle_life_max=50
walk_counter = 0
walk_counter_max = 2
walk_counter_player = 0
walk_counter_max_player = 2
combat_interval=20

if(__name__=="__main__"):
    collidables = [[ True
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH)]
    combat_counter=0
    particle_life=0
    othoni1=0
    othoni2=0
    floor = []
    number_of_particles = 10
    my_particles = []
    pygame.init()
    window_size=window_width,window_height=800,600
    map_size=800,600
    window=pygame.Surface((map_size))
    fog=pygame.Surface((window_size), pygame.SRCALPHA)
    background_rect = window.get_rect()
    s = pygame.display.set_mode((800,600),DOUBLEBUF)
    fog.fill((0,0,0,128)) 
    pygame.display.set_caption("TRYING THINGS")
    clock=pygame.time.Clock()
    mask = pygame.surface.Surface((864,864)).convert_alpha()
    mask.fill((0,0,0,255))
    fps=100
    block_group= pygame.sprite.Group()
    floor_group= pygame.sprite.LayeredUpdates()
    player_group=pygame.sprite.Group()
    items_group=pygame.sprite.Group()
    monster_group=pygame.sprite.Group()
    a_block=Block()
    a_block.set_image("images/knight_1.png")
    a_block.set_position(0,0)
    a_block.set_life(50)
    a_block.set_owner(a_block)
    player_group.add(a_block)
    running = True
    walls=[] # should change name to collidables
    running = True
    missiles = pygame.sprite.RenderUpdates()
    animation_counter=0
    #floor = pygame.image.load("images/floor.png")
    level=1
    make_map(floor_group,walls,a_block,monster_group,items_group,level,collidables)
    camera=[]
    camera.append(a_block.rect.x-50)
    camera.append(a_block.rect.y-50)
    radius = 200
    t = 255
    delta = 3
    offset=[]
    offset.append(a_block.rect.center[1])
    offset.append(a_block.rect.center[0])
    basicfont = pygame.font.SysFont(None, 20)
    while (running ):
        life=a_block.life
        if life<=0:
            running=False
        if not monster_group and life>0: # defeted all monsters -> procceed to new room
            collidables = [[ True for y in range(MAP_HEIGHT) ]   for x in range(MAP_WIDTH)]
            level += 1
            block_group= pygame.sprite.Group()
            floor_group= pygame.sprite.LayeredUpdates()
            player_group=pygame.sprite.Group()
            monster_group=pygame.sprite.Group()
            a_block=Block()
            a_block.set_image("images/knight_1.png")
            a_block.set_position(0,0)
            a_block.set_life(life)
            a_block.set_owner(a_block)
            player_group.add(a_block)
            running = True
            walls=[] # should change name to collidables
            running = True
            missiles = pygame.sprite.RenderUpdates()
            animation_counter=0
            #floor = pygame.image.load("images/floor.png")
            make_map(floor_group,walls,a_block,monster_group,items_group,level,collidables)
            camera=[]
            camera.append(a_block.rect.x-50)
            camera.append(a_block.rect.y-50)
            radius = 200
            t = 255
            delta = 3
            offset=[]
            offset.append(a_block.rect.center[1])
            offset.append(a_block.rect.center[0])
            basicfont = pygame.font.SysFont(None, 20)
        h = str(a_block.life)
        x = "HP: {} LEVEL: {}".format(h,level)
        text = basicfont.render(x, True, (0, 128, 0))
        offset[1]=(a_block.rect.center[1])
        offset[0]=(a_block.rect.center[0])
        n=randrange(0,6)
        m=randrange(0,6)
        x=randrange(0,20)
        light_pos_1=(camera[0]+65+n,camera[1]+80+m) #flickering
        light_pos=(camera[0]+65,camera[1]+80)
        radius = 200
        t = 255
        delta = 3
        missiles.update(walls)
        if walk_counter >= walk_counter_max:
            walk_counter = 0
        if walk_counter_player >= walk_counter_max_player:
            walk_counter_player = 0
        if particle_life > particle_life_max:
            my_particles[:]=[]
            particle_life=0
        if animation_counter >= animation_interval +1:
            animation_counter=0
        if combat_counter >= combat_interval +1:
            combat_counter=0
        for particle in my_particles:
            particle.move()
            particle.display()
        for item in items_group:
            if a_block.rect.colliderect(item):
                item.pick_up(item,a_block,items_group)
        for event in pygame.event.get():
            if (event.type==pygame.QUIT):
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if a_block.ammo>0:
                        missiles.add(Missile("images/missile_2.png",a_block.rect.center,(event.pos[0]+offset[0]/2-200,event.pos[1]+offset[1]/2-200),window,walls,monster_group,number_of_particles,my_particles ))
                        a_block.ammo -= 1
        key = pygame.key.get_pressed()
        for monster in monster_group:
            monster.ai(monster,a_block,walls,walk_counter,walk_counter_max,monster_group,collidables)
        combat(a_block,monster_group,player_group,my_particles,combat_counter)
        s.fill((0,0,0))
        mask.fill((0,0,0))
        s.blit(window,(200-offset[0]/2,200-offset[1]/2)) # dia 2 gia na min kanei scroll oso grigora oso kounieme.(dinei mia aisthish xorou anti apla na kouniete to map oso kouniete o pexths me apotelesma na fenete statheros o pexths)
        #s.blit(fog,(0,0))
        #s.blit(window, (background_rect.x+camera[0],background_rect.y+camera[1]),(0+camera[0],0+camera[1], 100, 100))
        if walk_counter_player == walk_counter_max_player-1:
            handle_event(event,key,a_block,block_group,player_group,walls,animation_counter,animation_interval,camera,monster_group,items_group,collidables)
        clock.tick(fps)
        #monster.render(monster_group,monster,a_block)
        floor_group.draw(window)
        items_group.draw(window)
        block_group.draw(window)
        player_group.draw(window)
        monster_group.draw(window)
        missiles.draw(window)

        for monster in monster_group:
           text2 = basicfont.render(str(monster.health), True, (255, 0, 0))
           window.blit(text2,(monster.rect.center[0]-10,monster.rect.center[1]-30))
        particle_life+=1
        animation_counter+=1
        walk_counter += 1
        walk_counter_player += 1
        combat_counter+=1
        while radius > 20:
            if x==4 or x==9 or x ==16 : #randomise the flicker
                light_pos_flick=light_pos_1
            else:
                light_pos_flick=light_pos
            pygame.draw.circle(mask,(21,11,0,t),(light_pos_flick),radius) #add color?
            t -= delta
            radius -= delta
        pygame.draw.circle(mask,(0,0,0,95),(light_pos),radius)
       #pygame.draw.circle(mask,(0,0,0,0),(400,275),50)
        s.blit(mask,(200-offset[0]/2,200-offset[1]/2))
        s.blit(text,(100,0))
        pygame.display.flip()
    pygame.quit
