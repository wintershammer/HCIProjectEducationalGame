import pygame
import math
import time
import random
from block import *
from item import*
from monster import*
from particles import *
from missile import *
from eventhandler import *
from pygame.locals import*
from level_generator import *
from combat import*
from shop import *
from questioner import*
import string

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
    randHPval1 = random.randint(20,40)
    randHPval2 = random.randint(20,40)    
    randHPval3 = random.randint(20,40)        
    Monster.healthPool.append(randHPval1)
    Monster.healthPool.append(randHPval2)
    Monster.healthPool.append(randHPval3)
    a_block=Block()
    a_block.set_image("images/knight_1.png")
    a_block.set_position(0,0)
    a_block.set_life(5)
    a_block.set_owner(a_block)
    player_group.add(a_block)
    pygame.mixer.music.load("sounds/Corfu_Ship_WaltzOldified.wav")
    spell1 = pygame.image.load("images/spell1.png").convert_alpha()
    spell2 = pygame.image.load("images/spell2.png").convert_alpha()
    spell3 = pygame.image.load("images/spell3.png").convert_alpha()
    selector = pygame.image.load("images/cursor.png").convert_alpha()
    powericon = pygame.image.load("images/powericon.png").convert_alpha()
    aoaicon = pygame.image.load("images/armoroa.png").convert_alpha()
    getrekt = selector.get_rect()
    spellrect1 = spell1.get_rect()
    spellrect2 = spell2.get_rect()
    spellrect3 = spell3.get_rect()
    running = True
    walls=[] 
    running = True
    missiles = pygame.sprite.RenderUpdates()
    animation_counter=0

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
    leinput = 0
    mousepos=0
    selectorA = 0
    pygame.mouse.set_pos(100,100)
    pygame.mouse.set_pos(100,100)
    pygame.mixer.music.set_volume(0.0)
    pygame.mixer.music.play(-1)
    print(Monster.healthPool)
    while (running ):
        pygame.mouse.set_visible(0)
        life=a_block.life
        if life<=0 and a_block.aoa <= 0: 
            running=False
        if not monster_group and life>0: 
            if level % 2 == 0:
              ShopGenerator(s)
              shop = False
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
            walls=[] 
            running = True
            missiles = pygame.sprite.RenderUpdates()
            animation_counter=0
            
            if(level == 2):
              make_boss_map(floor_group,walls,a_block,monster_group,items_group,level,collidables)
            else:
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
        for monster in monster_group:
            enemyhp = str(monster.health)
        x = "HP: {} LEVEL: {} ".format(h,level)
        text = basicfont.render(x, True, (0, 128, 0))
        offset[1]=(a_block.rect.center[1])
        offset[0]=(a_block.rect.center[0])
        n=random.randrange(0,6)
        m=random.randrange(0,6)
        x=random.randrange(0,20)
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
                if (event.button == 1 and a_block.get_ammo() > 0):
                    missiles.add(Missile("images/missile_2.png",a_block.rect.center,(event.pos[0],event.pos[1]),window,walls,monster_group,number_of_particles,my_particles,a_block.get_spldmg(),a_block.get_pie()) )
                    a_block.increment_ammo(-1)
                if event.button == 3:
                    for monster in monster_group:
                      if monster.rect.collidepoint(mousepos) and  monster.get_shield() > 0 and a_block.get_powercharge() > 0:
                        monster.increment_shield(-1)
                        a_block.increment_powercharge(-1)
        key = pygame.key.get_pressed()
        for monster in monster_group:
            monster.ai(monster,a_block,walls,walk_counter,walk_counter_max,monster_group,collidables)
            text2 = basicfont.render(monster.hptext, True, (255, 0, 0))
            window.blit(text2,(monster.rect.center[0]-10,monster.rect.center[1]-30))
        combat(a_block,monster_group,player_group,my_particles,combat_counter)
        s.fill((0,0,0))
        mask.fill((0,0,0))
        s.blit(window,(200-offset[0]/2,200-offset[1]/2)) # dia 2 gia na min kanei scroll oso grigora oso kounieme.(dinei mia aisthish xorou anti apla na kouniete to map oso kouniete o pexths me apotelesma na fenete statheros o pexths)
        if walk_counter_player == walk_counter_max_player-1:
            handle_event(event,key,a_block,block_group,player_group,walls,animation_counter,animation_interval,camera,monster_group,items_group,collidables,s,window)
        clock.tick(fps)
        floor_group.draw(window)
        items_group.draw(window)
        block_group.draw(window)
        player_group.draw(window)
        monster_group.draw(window)
        missiles.draw(window)
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
        s.blit(mask,(200-offset[0]/2,200-offset[1]/2))
        s.blit(text,(100,0))
        if a_block.get_ammoType() == 1 :
          x = str(a_block.get_ammo())
          text = basicfont.render(x, True, (0, 128, 102))
          text2 = basicfont.render("DMG: " + str(a_block.get_ammoDmg()), True, (0, 128, 102))          
          s.blit(spell1, (20,0))
          s.blit(text,(23,39))
          s.blit(text2,(60,39))          
        elif a_block.get_ammoType() == 2:
          x = str(a_block.get_ammo())
          text = basicfont.render(x, True, (0, 128, 102))
          text2 = basicfont.render("DMG: " + str(a_block.get_ammoDmg()), True, (0, 128, 102))              
          s.blit(spell2, (20,0))
          s.blit(text,(24,39))
          s.blit(text2,(60,39))           
        else:
          x = str(a_block.get_ammo())
          text = basicfont.render(x, True, (0, 128, 102))
          text2 = basicfont.render("DMG: " + str(a_block.get_ammoDmg()), True, (0, 128, 102))    
          s.blit(spell3, (20,0))
          s.blit(text,(24,39))
          s.blit(text2,(60,39)) 
        if a_block.get_powercharge()>0:
          x= str (a_block.get_powercharge())
          text=basicfont.render(x,True,(0,128,102))
          s.blit(powericon,(20,40))
          s.blit(text,(24,80))
        if a_block.get_invisibility() > 0:
          a_block.increment_invisibility(-1)
          x = str (a_block.get_invisibility())
          text=basicfont.render(x,True,(0,128,102))
          if(a_block.get_invisibility () % 5 >= 0): #every fifty frames blink image
            a_block.image=pygame.image.load('images/blank.png')
            a_block.image.set_colorkey((255,255,255))
        mousepos = pygame.mouse.get_pos()
        window.blit(selector,mousepos) # when you blit something at mousepoint it starts from its top left corner. so -32/2 to get it to print it with the middle under the mousepos
        pygame.display.flip()
    pygame.quit
