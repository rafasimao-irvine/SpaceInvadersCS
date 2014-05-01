
import pygame
from projectile import Projectile
from game_object import GameObject


class Invader(GameObject):
    
    MOVING_RIGHT = 0
    MOVING_RDOWN = 1
    MOVING_LEFT = 2
    MOVING_LDOWN = 3
    
    'Inits the invader'
    def __init__(self, projectile_list, x, y, max_side_move, max_down_move = 40):
        GameObject.__init__(self, x, y, 30, 30)
        self.speed = 0.05
        self.direction = self.MOVING_RIGHT
        
        self.projectile_list = projectile_list
        
        self.max_down_move = max_down_move
        self.max_side_move = max_side_move
        self._moved = max_side_move
        
        self.fire_delay = 0
    
    'Calculates the invader move'
    def _move(self, dt):
        #Quantifies the amount it must move
        move = round(self.speed*dt)
        self._moved -= move
        if self._moved < 0:
            move += self._moved
        
        #moves depending in the current direction
        if self.direction == self.MOVING_RIGHT:
            self.box.x += move
        elif self.direction == self.MOVING_RDOWN or self.direction == self.MOVING_LDOWN:
            self.box.y += move
        elif self.direction == self.MOVING_LEFT:
            self.box.x -= move
           
        #Determines the next direction
        if self._moved < 0:
            self._next_direction()
    
    def _next_direction(self):
        #sets the direction it will move to
        self.direction += 1
        if self.direction >3:
            self.direction = 0

        #sets the amount it must move
        if self.direction == self.MOVING_RDOWN or self.direction == self.MOVING_LDOWN:
            self._moved = self.max_down_move
        else:
            self._moved = self.max_side_move
   
    'Maybe used to speed up the invader velocity'
    def speedUp(self, amount = 1):
        self.speed += amount
    
    'Calculates the invader shoot'
    def _shoot(self, dt):
        #create a new projectile object moving downward
        if self.fire_delay > 30:
            self.fire_delay = 0
            
            self.projectile_list.append(Projectile(self.box.x+12.25, self.box.y+15, 2.5))
        
        #increases the fire time    
        else:
            self.fire_delay += 0.01*dt
    
    '''
    update() is called by the manager class individually for each invader, and will handle calling 
    that invader's _move() and _shoot()
    '''
    def update(self, dt):
        self._move(dt)
        self._shoot(dt)
                            
    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(230,230,230), 
                         (self.box.x, self.box.y, self.box.width, self.box.height))
