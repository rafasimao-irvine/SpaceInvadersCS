import pygame
from state import State
'''
Created on Apr 15, 2014

@author: ryanp
'''
class GameoverState(State):
    def __init__(self, start, screen, inputManager): 
        State.__init__(self, screen, inputManager)
        
        self.board_bounds = pygame.Rect(0,0, 950, 600)
        
        self.fontObj = pygame.font.Font('freesansbold.ttf', 42)
        
    def destroy(self): pass
    
    def update(self, dt): return 0
            
    def render(self):
        self.draw_intro_screen()
    
    'Draws the game over screen' 
    def draw_game_over_screen(self):
        self.screen.fill(pygame.Color(0,0,0))
        
        msgSurfaceObject = self.fontObj.render("Game Over", False, pygame.Color(205,255,205))
        msgRectObject = msgSurfaceObject.get_rect()
        msgRectObject.topleft = (425, 300)

        self.screen.blit(msgSurfaceObject, msgRectObject)