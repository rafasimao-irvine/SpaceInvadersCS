'''
Created on 14/04/2014

@author: rafaelsimao
@author: Minor Edits by Brian Paff
'''
import pygame
from Invaders import Invaders

from server import get_server

class InvadersManager():
    
    'Inits InvadersManager'
    def __init__(self):
        self.invaders_list = list()
        self.projectile_list = list()
        self.wave_number = 0;

        self.block_position = [0,0]
        self.spawn_time = 60
        self._create_block_of_invaders()

    def _create_block_of_invaders(self):
        for i in range(0, 15):
            self.invaders_list.append(Invaders(self.projectile_list, 100*i, i))

    def update(self, dt):
        self.update_projectiles(dt)
        self.update_invaders(dt)
        
        if Invaders.changed_direction:
            direction = self.invaders_list[0].direction
            if direction == Invaders.movingDownFromLeft:
                self.block_position[0] = 0
            elif direction == Invaders.movingDownFromLeft:
                self.block_position[0] = self.invaders_list[0].max_side_move
            elif direction == Invaders.movingLeft or direction == Invaders.movingRight:
                self.block_position[1] += self.invaders_list[0].max_down_move
            
            Invaders.changed_direction = False
            
            server = get_server()
            if server:
                server.send_msg({'invaders_changed_direction':direction,
                                'position':self.block_position,
                                'how_many_moves':self.invaders_list[0].howManyMoves})

    
        '''if self.spawn_time < 0:
            self.spawn_time = 60
            self._create_row_of_invaders()
        else:
            self.spawn_time -= 0.01*dt'''
                            
    def update_projectiles(self, dt):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.update(dt)
                
    def update_invaders(self, dt):
        if self.invaders_list.__len__() > 0: 
            for invader in self.invaders_list:
                invader.update(dt)
            self.move_block()
        else:
            self.new_wave_of_invaders()
    
    def move_block(self):
        direction = self.invaders_list[0].direction
        mvmtSpeed = self.invaders_list[0].mvmtSpeed
        if direction == Invaders.movingDownFromLeft or direction == Invaders.movingDownFromRight:
            self.block_position[1] += 1
        elif direction == Invaders.movingRight:
            self.block_position[0] += mvmtSpeed
        elif direction == Invaders.movingLeft:
            self.block_position[0] -= mvmtSpeed
            
    def move_all_invaders(self): pass
    
    def new_wave_of_invaders(self):
        self.wave_number += 1
        self._create_block_of_invaders()
        self.speedUp()
        self.block_position = (0,0)
        

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
            
    def changed_direction(self, new_direction, invaders_position, how_many_moves):
        x_offset = y_offset = 0
        block_position = self.block_position
        if block_position[0] != invaders_position[0] or block_position[1] != invaders_position[1]:
            x_offset = invaders_position[0] - block_position[0]
            y_offset = invaders_position[1] - block_position[1]
            self.block_position = invaders_position

        for invader in self.invaders_list:
            invader.direction = new_direction
            invader.box.x += x_offset
            invader.box.y += y_offset
            invader.howManyMoves = how_many_moves
        
