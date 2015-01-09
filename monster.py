import pygame
import math
import random
import time
from pygame.locals import*

class Monster(pygame.sprite.Sprite):

    healthPool = []
    count = 0

    
    #owner =0
    def __init__( self,color=(193,63,43),width = 32,height = 32):
        super(Monster,self).__init__()
        self.image=pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255,255,255))
        self.damage = 0
        self.attack_mode=0 # mallon tha to kano 1 gia melee 2 gia mage 3 gia range klp klp
        self.range=0
        self.health=0
        self.dx=0
        self.dy=0
        self.speed=1
        self.hptext = " "
        self.shield = 0
        self.twin = 0 # i should make a boss subclass!
        self.other_twin_dead = False
        Monster.count += 1


    def pickHP(self):
        x = random.randint(0,Monster.count)
        return Monster.healthPool[x]


    def set_attack_mode(self,mode):
        self.attack_mode=mode

    def set_range(self,value):
        self.range=value

    def get_attack_mode(self):
        return self.attack_mode

    def get_shield(self):
        return self.shield

    def increment_shield(self,value):
        self.shield += value
        
    def set_shield(self,value):
        self.shield = value
        
    def get_range(self):
        return self.range
    
    def create_orc(self):
        self.set_attack_mode(1)
        self.set_range(200)
        self.set_damage(1)
        #self.set_health(20)
        self.set_owner(self)
        self.set_image("images/orc_1.png")
    
    def create_tree(self):
        self.set_attack_mode(1)
        self.set_range(60)
        self.set_damage(10)
        #self.set_health(30)
        self.set_owner(self)
        self.set_image("images/treetemp.png")
        self.set_shield(1)

    def set_twin(self,value):
        self.twin = value

    def create_boss(self,name): # values are not balanced!
        if (name == 1):
            self.set_attack_mode(1)
            self.set_range(260)
            self.set_image("images/twinX.png")
            self.set_damage(1)
            self.health = 50
            self.hptext = str(self.health)
            self.set_owner(self)
            self.set_shield(0)
            self.set_twin(1)
        elif (name == 2):
            self.set_attack_mode(1)
            self.set_range(260)
            self.set_image("images/twinY.png")
            self.set_damage(1)
            self.health = 50
            self.hptext = str(self.health)
            self.set_owner(self)
            self.set_shield(0)
            self.set_twin(2)


    def increment_shield(self,value):
        self.shield += value
        
    def set_damage(self,value):
        self.damage=value
        
    def get_damage(self):
        return self.damage

    def get_shield(self):
        return self.shield
    
    def set_owner(self,owner):
        self.owner=owner
        
    def set_health(self,value):
        self.health=value
        var1 = random.randint(1,value)
        var2 = value - var1
        formatter = random.randint (0,2)
        if (formatter == 0):
            self.hptext = str(var1+1) + "+" + str(var2) + "= ?"
#        elif (formatter == 1):
#            self.hptext = "?" + str(var2) + "= ?"
        else:
            compositter = random.randint(1,var2)
            composite = var2/compositter
            print value, var1+1, composite,compositter, "---"
            self.hptext = str(var1+1) + "+" + str(composite) + "*" + str(compositter) + "= ?"
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

    def move_towards(self, target_x, target_y,walls,monster,monster_group,collidables):
        #vector from this object to the target, and distance
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        minDist = 300
        for monster in monster_group:
            dist =  math.sqrt(math.pow((self.rect.x - monster.rect.x)^2, 2) + math.pow((self.rect.y - monster.rect.y)^2, 2))
            sqrdist = math.sqrt(dist)
            if dist < minDist and dist > 32:
                minDist = dist
                minX = monster.rect.x
                minY = monster.rect.y
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        minAllowed = 40
        if self.twin > 0 :
            minAllowed = 100
        
        if collidables[self.rect.x/32+dx+1][self.rect.y/32+dy+1] == False and minDist > minAllowed : #hmm panta tha kolane ean einai sto minDist :/
            self.dx=dx
            self.dy=dy
            self.move(dx*self.speed, dy*self.speed)
#        else:
#            if collidables[self.rect.x/32+dx+1][self.rect.y/32+dy+1] == False:
#             self.move_towards(target_x*-1,target_y*-1,walls,monster,monster_group,collidables)
        if minDist < minAllowed:
            dx = target_x - minX
            dy = target_y - minY
            distance = math.sqrt(dx ** 2 + dy ** 2)
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
            if collidables[self.rect.x/32+dx+1][self.rect.y/32+dy+1] == False :
                self.dx= -dx
                self.dy= -dy
                self.move(dx*self.speed, dy*self.speed)
    def knockback(self,knockback,walls,monster_group):
        #for wall in walls:
        #    if pygame.sprite.collide_mask(self,wall) != None:
        #        monster_group.remove(self.owner)
                #print"you knock the orc into the wall and kill him"
        if self.dx > 0: # Moving right; Hit the left side of the wall
            self.move(-knockback,0)
        if self.dx < 0: # Moving left; Hit the right side of the wall
            self.move(knockback,0)
        if self.dy > 0: # Moving down; Hit the top side of the wall
            self.move(0,-knockback)
        if self.dy < 0: # Moving up; Hit the bottom side of the wall
            self.move(0,knockback)
        # diagonals
        if self.dy>0 and self.dx>0:
            self.move(-knockback,-knockback)
        if self.dy<0 and self.dx>0:
            self.move(-knockback,knockback)
        if self.dy<0 and self.dx<0:
            self.move(knockback,knockback)
        if self.dy>0 and self.dx<0:
            self.move(knockback,-knockback)


    
    def ai(self,monster,target,walls,walk_counter,walk_counter_max,monster_group,collidables):
        if monster.distance_to(target) <= monster.range and monster.distance_to(target) >= 20 and walk_counter == walk_counter_max-1:
                monster.move_towards(target.rect.x, target.rect.y,walls,monster,monster_group,collidables)

    def old_health(self,health):
        self.health = health


##    def render(self,monster_group,monster,target):
##        rendered_once = True
##        if monster.distance_to(target) <= 70 and self.health>=0 and rendered_once:
##            render_once = False
##            monster_group.add(self.owner)

    def death(self,monster_group,damage,walls):
        self.set_range(999)
        #self.range=100 # the monster is alert of your presence
        if self.health>20:
            self.knockback(5,walls,monster_group)
        else:
            self.speed=3
            #print "ORC IS ENRAGED"
        if self.shield == 0:
            if damage == self.health :
                self.health -= damage
            elif damage == 5: #5 is melee test damage for now. i should be getting this from player.get_meleeDmg()
                self.health -= damage

        self.hptext = str(self.health) #if you succeeded in killing them with your spell then well played! otherwise you now have to kill them with your melee attack >: booring
        print (self.hptext)

        if self.health <= 0:
            monster_group.remove(self.owner)

    def death_twins(self,monster_group,damage,walls): # TESTING:once i move them to their own class I will have no need for such awkward code.

        self.hptext = str(self.health)
        print (self.hptext)
        
        if(self.twin == 2):

            if(self.other_twin_dead == True):              
                self.health -= int(damage/3)
        else:
            self.health -= int(damage/3) #bosses are tough!
        
        if self.health <= 0:
            if(self.twin == 1):
                for monster in monster_group :
                    if monster.twin == 2:
                        secondTwin = monster
                        secondTwin.other_twin_dead = True
            monster_group.remove(self.owner)        



        
        
