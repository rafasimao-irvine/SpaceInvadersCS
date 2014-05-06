'''
Created on May 6, 2014

@author: Owner
'''

from invaders_manager import InvadersManager

    
class Model:
    
    def __init__(self):
        self.invaders = InvadersManager()
        
            
    def update(self,dt):
        invaders.update_invaders()
            
    
