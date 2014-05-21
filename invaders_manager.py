'''
Created on 14/04/2014

@author: rafaelsimao
@author: Minor Edits by Brian Paff
'''
import pygame
from Invaders import Invaders

from server import get_server

class InvadersManager():
    
    movingRight=0
    movingDownFromRight=1
    movingLeft=2
    movingDownFromLeft=3
    
    'Inits InvadersManager'
    def __init__(self):
        self.invaders_list = list()
        self.projectile_list = list()
        self.wave_number = 0;
        self.num_of_invaders_per_wave = 15;

        self.max_down_move = 40
        self.max_side_move = 625
        self.howManyMoves = self.max_side_move
        self.direction = self.movingRight
        self.sideSpeedMultiplier = 0.04
        self.sideSpeed = 0.04
        self.downSpeed = 0.01
        self.movement = [self.sideSpeed,0]

        self.block_position = [0,0]
        self._create_block_of_invaders()

    def _create_block_of_invaders(self):
        for i in range(0, self.num_of_invaders_per_wave):
            self.invaders_list.append(Invaders(self.projectile_list, self.block_position, i, self.movement))
      
    def update(self, dt):
        self._update_projectiles(dt)
        self._update_invaders(dt)
        self._move_block(dt)
                            
    def _update_projectiles(self, dt):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.update(dt)
                
    def _update_invaders(self, dt):
        if self.invaders_list.__len__() > 0: 
            for invader in self.invaders_list:
                invader.update(dt)
        else:
            self.new_wave_of_invaders()
    
    def _move_block(self, dt):
        self.howManyMoves = round(self.howManyMoves - abs(self.movement[0]*dt))
        self.howManyMoves = round(self.howManyMoves - self.movement[1]*dt)
        
        self.block_position[0] += round(self.movement[0] *dt)
        self.block_position[1] += round(self.movement[1] *dt)
        
        if self.howManyMoves < 0:
            self._next_direction()
            
    def _next_direction(self):
        self.direction += 1
        if self.direction > 3:
            self.direction = 0
            
        extra_moves = [0,0]

        if self.direction == self.movingDownFromRight:
            extra_moves[0] = self._set_new_direction_moves(self.max_down_move, [0,self.downSpeed])
        elif self.direction == self.movingDownFromLeft:
            extra_moves[0] = -self._set_new_direction_moves(self.max_down_move, [0,self.downSpeed]) 
        elif self.direction == self.movingRight:
            extra_moves[1] = self._set_new_direction_moves(self.max_side_move, [self.sideSpeed,0]) 
        elif self.direction == self.movingLeft:
            extra_moves[1] = self._set_new_direction_moves(self.max_side_move, [-self.sideSpeed,0]) 
            
        # updates the invaders with the new movement
        for invader in self.invaders_list:
            invader.movement = self.movement
            invader.box.x += extra_moves[0]
            invader.box.y += extra_moves[1]
            
        self.block_position[0] += extra_moves[0]
        self.block_position[1] += extra_moves[1]
            
        server = get_server()
        if server:
            server.send_msg({'invaders_changed_direction':self.direction,
                             'position':self.block_position,
                             'how_many_moves':self.howManyMoves})

    def _set_new_direction_moves(self, howManyMoves, movement):
        extra = self.howManyMoves
        self.howManyMoves = howManyMoves
        self.movement = movement
        return extra
    
            
    def new_wave_of_invaders(self):
        self.wave_number += 1
        self.speedUp(self.wave_number+1)
        self.block_position = [0,0]
        self.howManyMoves = self.max_side_move
        self.direction = self.movingRight
        self.movement = [self.sideSpeed,0]
        self._create_block_of_invaders()
         
       
    def speedUp(self, amount = 1.10):
        self.sideSpeed = self.sideSpeedMultiplier*amount
        

    def render(self, screen):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.render(pygame.Color(255, 0, 0), screen)

        if self.invaders_list.__len__() > 0: 
            for invader in self.invaders_list:
                if not invader.marked:
                    invader.render(screen)
    
    
    def get_dead_invaders_numbers(self):
        invaders_list = self.invaders_list
        dead_invaders_numbers = list()
        
        for i in range(0, self.num_of_invaders_per_wave):
            dead_invaders_numbers.append(i)
            
        for invader in invaders_list:
            dead_invaders_numbers.remove(invader.invader_number)
            
        return dead_invaders_numbers
    

    def _set_movement_by_direction(self, direction):
        if direction == self.movingDownFromRight:
            self.movement = [0,self.downSpeed]
        elif direction == self.movingDownFromLeft:
            self.movement = [0,self.downSpeed]
        elif direction == self.movingRight:
            self.movement = [self.sideSpeed,0] 
        elif direction == self.movingLeft:
            self.movement = [-self.sideSpeed,0]
        
            
    '''****** Network Message ******'''
    
    def changed_direction(self, new_direction, invaders_position, how_many_moves):
        x_offset = y_offset = 0
        block_position = self.block_position
        if block_position[0] != invaders_position[0] or block_position[1] != invaders_position[1]:
            x_offset = invaders_position[0] - block_position[0]
            y_offset = invaders_position[1] - block_position[1]
            self.block_position = invaders_position
            
        self._set_movement_by_direction(new_direction)
            
        self.direction = new_direction
        self.howManyMoves = how_many_moves

        for invader in self.invaders_list:
            invader.box.x += x_offset
            invader.box.y += y_offset
            invader.movement = self.movement
            
            
    def sync_invaders(self, wave_number, block_position, dead_invaders, direction, howManyMoves):
        # new attributes
        self.block_position = block_position
        self.wave_number = wave_number
        self.direction = direction
        self.howManyMoves = howManyMoves

        # new invaders        
        del self.invaders_list[:]
        self._create_block_of_invaders()
        
        
        invaders_to_remove = list()
        for i in dead_invaders:
            invaders_to_remove.append(self.invaders_list[i])
        for r in invaders_to_remove:
            self.invaders_list.remove(r)
            
        # new movements
        self._set_movement_by_direction(direction)
        self.speedUp(wave_number+1)
        for invader in self.invaders_list:
            invader.movement = self.movement
        