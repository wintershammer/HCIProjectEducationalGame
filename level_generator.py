import pygame
import math
import random
from item import*
from monster import*
import time
from block import *
from pygame.locals import*


MAP_HEIGHT= 25
MAP_WIDTH=19
ROOM_MAX_SIZE = 6
ROOM_MIN_SIZE = 5
MAX_ROOMS = 5


class Rect:
    # abstraction tou domatiou os Rect(angle)
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)






        
def create_room(room,floor_group,collidables):
    global map
    
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].set_image("images/floor.png")
            map[x][y].set_position(x*32,y*32)
            floor_group.add(map[x][y])
            collidables[x][y]=False

def create_boss_room(floor_group,collidables):
    global map
    
    for x in range(1, MAP_WIDTH-1):
        for y in range(1, MAP_HEIGHT-1):
            map[x][y].set_image("images/floor.png")
            map[x][y].set_position(x*32,y*32)
            floor_group.add(map[x][y])
            collidables[x][y]=False

def create_h_tunnel(x1, x2, y,floor_group,collidables):
    global map
    
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].set_image("images/floor.png")
        map[x][y].set_position(x*32,y*32)
        floor_group.add(map[x][y])
        collidables[x][y]=False
        map[x+1][y+1].set_image("images/floor.png")
        map[x+1][y+1].set_position((x+1)*32,(y+1)*32)
        floor_group.add(map[x+1][y+1])
        collidables[x+1][y+1]=False
 
def create_v_tunnel(y1, y2, x,floor_group,collidables):
    global map
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].set_image("images/floor.png")
        map[x][y].set_position(x*32,y*32)
        floor_group.add(map[x][y])
        collidables[x][y]=False



def make_map(floor_group,walls,a_block,monster_group,items_group,level,collidables):
    global map, player
 
    #gemise ton pinaka me blocks ftiaxe ta rooms allazontas ta blocks
    map = [[ Block()
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH)]


    rooms = []
    num_rooms = 0
 
    for r in range(MAX_ROOMS):
        
        w = random.randint(ROOM_MIN_SIZE,ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE,ROOM_MAX_SIZE)
        
        x = random.randint(0, MAP_WIDTH - w - 1)
        y = random.randint(0, MAP_WIDTH - h - 1)
 
        
        new_room = Rect(x, y, w, h)
 
        
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
 
        if not failed:
            
 
            
            create_room(new_room,floor_group,collidables)
 
            
            (new_x, new_y) = new_room.center()
 
            if num_rooms == 0:
                
                a_block.rect.x=new_x*32
                a_block.rect.y= new_y*32
            else:
                
                
 
                
                (prev_x, prev_y) = rooms[num_rooms-1].center()


                
                populateDungeon(map,new_x,new_y,5,monster_group,items_group,2,level,False)

                 
                
                if random.randint(0, 1) == 1:
                    
                    create_h_tunnel(prev_x, new_x, prev_y,floor_group,collidables)
                    create_v_tunnel(prev_y, new_y, new_x,floor_group,collidables)
                else:
                    
                    create_v_tunnel(prev_y, new_y, prev_x,floor_group,collidables)
                    create_h_tunnel(prev_x, new_x, new_y,floor_group,collidables)
 
            
            rooms.append(new_room)
            num_rooms += 1
    for x in range(0, MAP_WIDTH):
        for y in range(0,MAP_HEIGHT):
            if collidables[x][y] == True :
                map[x][y].set_image("images/wall_n.png")
                map[x][y].set_position(x*32,y*32)
                floor_group.add(map[x][y])
            
    collide_creator(collidables,walls,map)



def make_boss_map(floor_group,walls,a_block,monster_group,items_group,level,collidables): # i will merge this with make_map when its done!
    global map, player
 
    
    map = [[ Block()
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH)]


    rooms = []
    num_rooms = 0
 

    create_boss_room(floor_group,collidables)
    populateDungeon(map,MAP_WIDTH/2,MAP_HEIGHT/2,2,monster_group,items_group,2,level,True)
    a_block.rect.x = 60
    a_block.rect.y = 60
    
    for x in range(0, MAP_WIDTH):
        for y in range(0,MAP_HEIGHT):
            if collidables[x][y] == True :
                map[x][y].set_image("images/wall_n.png")
                map[x][y].set_position(x*32,y*32)
                floor_group.add(map[x][y])
            
    collide_creator(collidables,walls,map)



def collide_creator(collidables,walls,map):
    for i in range (0,MAP_WIDTH):
        for j in range(0,MAP_HEIGHT):
            if collidables[i][j]==True:
                walls.append(map[i][j])




def populateDungeon(map,room_x,room_y,max_monsters,monster_group,items_group,max_items,level,boss_room):
    monsters = []
    numtrees = 0
    for i in range (0,2):
        if(boss_room == False):
            manster= Monster()
            monsters.append(manster)
            #print y
        else:
            twinX = Monster()
            monsters.append(twinX)
            twinY = Monster()
            monsters.append(twinY)
    for monster in monsters:
        if(boss_room == False):
            randx=random.randint(-50,50)
            randy=random.randint(-50,50)
            if level > 1:
                chooser = random.randint(0,1)
                if chooser == 1:
                    monster.create_orc()
                else:
                    monster.create_tree()
            else:
                monster.create_orc()
            monster.set_position(room_x*32+randx,room_y*32+randy)
            monster_group.add(monster)
            monster.set_health(20+level*5)
        else:
            if(monster == twinX):
                monster.create_boss(1)
            else:
                monster.create_boss(2)
            if(monster == twinX):
                monster.set_position(32 * MAP_WIDTH/2,32 * MAP_HEIGHT/2)
            else:
                monster.set_position(20 * MAP_WIDTH/2,20 * MAP_HEIGHT/2)
            monster_group.add(monster)
            
    x = random.randint(1,5)
##    if x == 2 or x == 5:
##        for i in range(0,max_items):
##            bow = Item()
##            bow.set_image("images/potion.png")
##            if y==1:
##                bow.set_image("images/bow_1.png")
##            bow.set_position(room_x*32+x*2,room_y*32)
##            bow.set_owner(bow)
##            bow.effects(y+1,5)
##            items_group.add(bow)

    for i in range (0,max_items):
        newItem = Item()
        if x == 1:
            newItem.set_image("images/potion.png")
            newItem.set_position(room_x*32+x*2,room_y*32)
            newItem.set_owner(newItem)
            newItem.effects(x,5)
            items_group.add(newItem)
        elif x == 2:
            newItem.set_image("images/bow_1.png")
            newItem.set_position(room_x*32+x*2,room_y*32)
            newItem.set_owner(newItem)
            newItem.effects(x,5)
            items_group.add(newItem)
        elif x == 4:
            newItem.set_image("images/armoroa.png")
            newItem.set_position(room_x*32+x*2,room_y*32)
            newItem.set_owner(newItem)
            newItem.effects(4,5)
            items_group.add(newItem)
        elif (x == 5):
            newItem.set_image("images/pie.png")
            newItem.set_position(room_x*32+x*2,room_y*32)
            newItem.set_owner(newItem)
            newItem.effects(5,0)
            items_group.add(newItem)
        
