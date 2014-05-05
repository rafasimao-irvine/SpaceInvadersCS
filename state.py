from input_listener import InputListener

'''
Abstract class used as model to the state classes
'''
class State(InputListener):
    
    def __init__(self, screen, inputManager, networkHandler): 
        self.screen = screen
        self.networkHandler = networkHandler
        self.inputManager = inputManager
        inputManager.attach(self)
        
    def destroy(self): pass
    
    def update(self, dt): return 0
    def render(self): pass
