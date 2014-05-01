'''
Created on Apr 9, 2014

@author: ryanp
'''
import pygame
from game_object import GameObject

class Projectile(GameObject):

    'Inits the Projectile attributes'
    def __init__(self, xpos, ypos, speed):
        GameObject.__init__(self, xpos, ypos, 5, 30)
        #self.x = xpos
        #self.y = ypos
        self.speed = speed
        self.dt = 5
    
    'Moves the Projectile'
    def move(self):
        self.box.top += self.speed*self.dt

    'Draws the Projectile in the screen'
    def render(self, color, screen):
        pygame.draw.rect(screen, color, (self.box.left, self.box.top, self.box.width, self.box.height)) 
