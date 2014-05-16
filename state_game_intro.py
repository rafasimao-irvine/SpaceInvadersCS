import pygame
from state import State
'''
Created on Apr 15, 2014

@author: ryanp
'''
class StateGameIntro(State):
    def __init__(self, start, screen, inputManager): 
        State.__init__(self, screen, inputManager)
        
        self.start = start
        
        self.board_bounds = pygame.Rect(0,0, 950, 600)
        
        self.fontObj1 = pygame.font.Font('freesansbold.ttf', 42)
        self.fontObj2 = pygame.font.Font('freesansbold.ttf', 24)
        
    def destroy(self): pass
    
    def update(self, dt):
        if self.start != 100:
            self.start+=1
            
    def render(self):
        self.draw_intro_screen()
    
    'Draws the intro screen' 
    def draw_intro_screen(self):
        self.screen.fill(pygame.Color(0,0,0))
        
        msgSurfaceObject1 = self.fontObj1.render("Space Invaders", False, pygame.Color(205,255,205))
        msgRectObject1 = msgSurfaceObject1.get_rect()
        msgRectObject1.topleft = (425, 300)
        
        msgSurfaceObject2 = self.fontObj2.render("Loading: " + str(self.start) + "%", False, pygame.Color(205,255,205))
        msgRectObject2 = msgSurfaceObject2.get_rect()
        msgRectObject2.topleft = (425, 400)

        self.screen.blit(msgSurfaceObject1, msgRectObject1)
        self.screen.blit(msgSurfaceObject2, msgRectObject2)
