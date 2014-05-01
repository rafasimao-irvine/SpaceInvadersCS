import pygame
from input_listener import InputListener
from projectile import Projectile
from game_object import GameObject

class Player(GameObject, InputListener):
    
    'Inits the player attributes'
    def __init__(self):
        GameObject.__init__(self, 425.0, 500.0, 60, 60)    

        self.life = 5
        self.score = 0
        
        self.speed = 0.25
    
        self.projectile_list = list()
        self.fire_delay = 15
        
        self.move_right = self.move_left = self.fire_shot = False
    
    'Makes the player actions _move and fire'
    def update(self, dt):
        self._move(dt) 
        self._shoot()
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.move()
        if self.fire_delay < 15:
            self.fire_delay += 1
            
    'Moves the player, based in the current pressed buttons'
    def _move(self, dt):
        if self.move_left and self.box.left > 0:
            self.box.left -= self.speed*dt
        elif self.move_right and self.box.left < 900:
            self.box.left += self.speed*dt
     
    'Allows the player to fire projectiles if correct button is pressed'
    def _shoot(self):
        if self.fire_shot and self.fire_delay == 15:
            projectile = Projectile(self.box.left+22.5, self.box.top, -2.5)
            self.projectile_list.append(projectile)
            #print(self.projectile_list.__len__())
            self.fire_delay = 0
    
    'Draws the player and projectiles on the screen'
    def render(self, screen):
        if self.projectile_list.__len__() > 0: 
            for shot in self.projectile_list:
                shot.render(pygame.Color(0, 191, 255), screen)
        pygame.draw.rect(screen, pygame.Color(255,255,255), 
                         (self.box.left,self.box.top,self.box.width,self.box.height))
        
        #Draws the player life
        for i in range(0,self.life):
            pygame.draw.rect(screen, pygame.Color(255,80,80),
                             (self.box.left+i*13,self.box.bottom+2,10,10))
    
    def receive_hit(self):
        self.life -=1
        
    def increase_score(self, points):
        self.score += points

    'Receives inputs and treats them if they corresponds to moving or firing'
    def receive_input(self, event):
        #Starts moving
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left = True
            elif event.key == pygame.K_d:
                self.move_right = True
        #Finishes moving
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move_left = False
            elif event.key == pygame.K_d:
                self.move_right = False
        #Starts firing projectile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.fire_shot = True
        #Finishes firing projectile
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.fire_shot = False
