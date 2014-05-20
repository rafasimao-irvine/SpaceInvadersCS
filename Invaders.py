'''
Created on Apr 9, 2014

@author: Brian Paff
94135229
'''

'''
make collisions happen, add RNG to make the invaders shoot at different times
'''
import pygame
import random
from projectile import Projectile
from game_object import GameObject
random.seed()

from server import get_server

class Invaders(GameObject):
    
    '''
    Invader is going to spawn a new enemy on the screen. It takes how many enemies are spawned,
    then divides that number by the max number of invaders we want on a line  and takes the floor 
    of it. This will give us the amount of lines down we should drop that spawned invader.
    We then find out how many invaders are currently on the current line we're working with by 
    taking that floor we just calculated, multiplying it by the max amount of invaders, and
    then subtracting that product from the amount of invaders that have been spawned. We then _move
    this invader over the appropriate amount of spaces.
    '''
    def __init__(self, projectiles, x, amountOfInvadersSpawned, movement):
        maxInvaders = 5
        #check if there are destroyed invaders you can replace
        temp = amountOfInvadersSpawned/maxInvaders
        self.y = 50 * temp
        temp2 = temp * maxInvaders
        #amountOfInvadersOnThisLine
        aOIOTL = amountOfInvadersSpawned - temp2
        self.x= 50 * aOIOTL
        GameObject.__init__(self, self.x, self.y, 30, 30)
        
        self.projectile_list = projectiles
        
        self.movement = movement
        
        self.shotDelay = random.randrange(1000,5000)
        self.timeSinceLastShot = 0
        
        self.marked = False
    
        '''
    Move changes the position of the invader by taking its current position, and adds the current
    movement speed to that old position value. If it hits the side of the game board or it will
    _move past it during this method call, it should drop down one line and reverse direction.
    '''
    def _move(self, dt):
        self.box.x += round(self.movement[0] *dt)
        self.box.y += round(self.movement[1] *dt)
            
    
    '''
    _shoot checks to see if a given interval has passed since the last time this invader fired,
    if it has, then it should make a projectile object
    '''
    def _shoot(self, dt):
        if self.timeSinceLastShot > self.shotDelay:
            self.timeSinceLastShot = 0
            
            self.projectile_list.append(Projectile(self.box.x+12.25, self.box.y+15, 0.4))
            
            server = get_server()
            if server:
                server.send_msg({'invaders_shoot':[self.box.x+12.25, self.box.y+15, 0.4]})
            
        #increases the fire time    
        else:
            self.timeSinceLastShot = self.timeSinceLastShot + dt
    '''
    update() is called by the manager class individually for each invader, and will handle calling 
    that invader's _move() and _shoot()
    '''
    def update(self, dt):
        self._move(dt)
        if get_server():
            self._shoot(dt)
    
    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(230,230,230), 
                         (self.box.x, self.box.y, self.box.width, self.box.height))

    