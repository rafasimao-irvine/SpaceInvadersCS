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
        self.fontObj3 = pygame.font.Font('freesansbold.ttf', 18)
        
    def destroy(self): pass
    
    def update(self, dt):
        if self.start != 100:
            self.start+=5
            
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
        
        msgSurfaceObject3 = self.fontObj3.render("Controls: 'A' - move left", False, pygame.Color(205,255,205))
        msgRectObject3 = msgSurfaceObject3.get_rect()
        msgRectObject3.topleft = (425, 450)
        
        msgSurfaceObject4 = self.fontObj3.render("                  'D' - move right", False, pygame.Color(205,255,205))
        msgRectObject4 = msgSurfaceObject4.get_rect()
        msgRectObject4.topleft = (425, 475)
        
        msgSurfaceObject5 = self.fontObj3.render("                  'SPACE' - fire", False, pygame.Color(205,255,205))
        msgRectObject5 = msgSurfaceObject5.get_rect()
        msgRectObject5.topleft = (425, 500)

        self.screen.blit(msgSurfaceObject1, msgRectObject1)
        self.screen.blit(msgSurfaceObject2, msgRectObject2)
        self.screen.blit(msgSurfaceObject3, msgRectObject3)
        self.screen.blit(msgSurfaceObject4, msgRectObject4)
        self.screen.blit(msgSurfaceObject5, msgRectObject5)
