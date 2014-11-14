import pygame
import math
import random
import time
from pygame.locals import*




def particle_create(coord,number_of_particles,my_particles,window):
    for n in range(number_of_particles):
        size = random.randint(1,2)
        x = random.randint(size, 100-size)
        y = random.randint(size, 100-size)
        particle = Particle(coord, size,window)
        particle.speed = random.random()
        particle.angle = random.uniform(0, math.pi*2)
        my_particles.append(particle)


class Particle():
    def __init__(self, (x, y), size,window):
        self.window = window
        self.x = x
        self.y = y
        self.size = size
        self.colour = (255, 0, 0)
        self.thickness = 0 # 0 gia disko 1 gia kiklo
        self.speed = 0
        self.angle = 0
    def display(self):
        pygame.draw.circle(self.window, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
