'''
Created on 14/04/2014

@author: rafaelsimao
@author: Minor Edits by Brian Paff
'''
import pygame
from Invaders import Invaders

class InvadersManager():
    
    'Inits InvadersManager'
    def __init__(self):
        self.invaders_list = list()
        self.projectile_list = list()
        self.wave_number = 0;

        self.spawn_time = 60
        self._create_block_of_invaders()

    def _create_block_of_invaders(self):
        for i in range(0, 15):
            self.invaders_list.append(Invaders(self.projectile_list, 100*i, i))

    def update(self, dt):
        self.update_projectiles(dt)
        self.update_invaders(dt)
        
        '''if self.spawn_time < 0:
            self.spawn_time = 60
            self._create_row_of_invaders()
        else:
            self.spawn_time -= 0.01*dt'''
                            
    def update_projectiles(self, dt):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.move()
                
    def update_invaders(self, dt):
        if self.invaders_list.__len__() > 0: 
            for invader in self.invaders_list:
                invader.update(dt)
        else:
            self.wave_number += 1
            self._create_block_of_invaders()
            self.speedUp()
        

    def render(self, screen):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.render(pygame.Color(255, 0, 0), screen)

        if self.invaders_list.__len__() > 0: 
            for invader in self.invaders_list:
                invader.render(screen)
    
    def speedUp(self):
        for i in self.invaders_list:
            i.speedUp(self.wave_number)
