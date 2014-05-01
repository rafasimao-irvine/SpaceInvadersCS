import pygame

class GameObject():
    
    def __init__(self, x, y, width, height):
        self.box = pygame.Rect(x, y, width, height)
    
    def update(self, dt): pass
    def render(self, screen): pass
    
    def get_collision_box(self):
        return self.box
        
    def is_colliding_with(self, other):
        return self.box.colliderect(other.get_collision_box())