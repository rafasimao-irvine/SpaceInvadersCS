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


class Invaders(GameObject):
    
    movingRight=0
    movingDownFromRight=1
    movingLeft=2
    movingDownFromLeft=3
    '''
    Invader is going to spawn a new enemy on the screen. It takes how many enemies are spawned,
    then divides that number by the max number of invaders we want on a line  and takes the floor 
    of it. This will give us the amount of lines down we should drop that spawned invader.
    We then find out how many invaders are currently on the current line we're working with by 
    taking that floor we just calculated, multiplying it by the max amount of invaders, and
    then subtracting that product from the amount of invaders that have been spawned. We then _move
    this invader over the appropriate amount of spaces.
    '''
    def __init__(self, projectiles, x, amountOfInvadersSpawned):
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
        self.max_down_move = 200
        self.max_side_move = 625
        self.howManyMoves = self.max_side_move
        self.direction = self.movingRight
        self.mvmtSpeed = 4
        
        self.shotDelay = random.randrange(1000,3000)
        self.timeSinceLastShot = 0
    
        '''
    Move changes the position of the invader by taking its current position, and adds the current
    movement speed to that old position value. If it hits the side of the game board or it will
    _move past it during this method call, it should drop down one line and reverse direction.
    '''
    def _move(self, dt):
        self.howManyMoves = round(self.howManyMoves - self.mvmtSpeed)
            
        if self.direction == self.movingDownFromLeft or self.direction == self.movingDownFromRight:
            self.box.y = self.box.y + 1
            self.howManyMoves = self.howManyMoves - 1
        elif self.direction == self.movingRight:
            self.box.x = self.box.x + self.mvmtSpeed
            #self.howManyMoves = self.howManyMoves - 1
        elif self.direction == self.movingLeft:
            self.box.x = self.box.x - self.mvmtSpeed
            #self.howManyMoves = self.howManyMoves - 1
            
        if self.howManyMoves < 0:
            self._next_direction()

    
    '''
    speedUp() is called by the manager class, and will make the invaders _move faster when one has 
    been killed
    '''
    def speedUp(self, amount = 1.10):
        a= self.mvmtSpeed * amount
        self.mvmtSpeed = a
    
    '''
    _shoot checks to see if a given interval has passed since the last time this invader fired,
    if it has, then it should make a projectile object
    '''
    def _shoot(self, dt):
        if self.timeSinceLastShot > self.shotDelay:
            self.timeSinceLastShot = 0
            
            self.projectile_list.append(Projectile(self.box.x+12.25, self.box.y+15, 2.5))
        
        #increases the fire time    
        else:
            self.timeSinceLastShot = self.timeSinceLastShot + dt
    '''
    update() is called by the manager class individually for each invader, and will handle calling 
    that invader's _move() and _shoot()
    '''
    def update(self, dt):
        self._move(dt)
        self._shoot(dt)
        #if self.projectile_list.__len__() > 0: 
        #    for shot in self.projectile_list:
        #        shot.move()
        #if self.fire_delay < 15:
        #    self.fire_delay+=1
    
    def _next_direction(self):
        self.direction = self.direction + 1
        if self.direction > 3:
            self.direction = 0

       
        if self.direction == self.movingDownFromRight or self.direction == self.movingDownFromLeft:
            self.howManyMoves = self.max_down_move
        else:
            self.howManyMoves = self.max_side_move
                            
    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(230,230,230), 
                         (self.box.x, self.box.y, self.box.width, self.box.height))

    