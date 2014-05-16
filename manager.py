import pygame
from input_manager import InputManager
from state_game_intro import StateGameIntro
from state_game import StateGame

from client import start_client, periodic_poll

#initiate the pygame
pygame.init()
fpsClock = pygame.time.Clock()
#print("initializing clock: ", fpsClock)

#Manager class
class Manager:

    ##Screen
    width, height = 950, 600
    size = width, height
    
    screen  = pygame.display.set_mode(size)

    pygame.display.set_caption("SpaceInvaders")        

    #InputManager
    inputManager = InputManager()
    
    game_state = StateGame(screen, inputManager)
    #NetworkHandler
    client = start_client(game_state)

    #Introduction state
    state = StateGameIntro(0, screen, inputManager)
    
    #Game started check
    game_started = False
    #Main Loop
    def _run(self):
        self.gameOn = True
        
        while self.gameOn:
            dt = fpsClock.tick(30)

            #Network
            periodic_poll()

            #Inputs
            self.inputManager.update()
            
            if self.game_started == False:
                if self.state.start == 100:
                    self.set_state(self.game_state)
                    self.game_started = True
                    if self.client != None:
                        self.client.do_send({'join':self.game_state.player.box.topleft})
            
            #Updates
            self.update(dt)
                
            #Renders, put in the screen
            self.render()
        
    
    #Update
    def update(self, dt):
        #state updates
        new_state = self.state.update(dt)
        if (new_state == 0):
            return
       
    def set_state(self, state):
        self.state.destroy()
        self.state = state
    
    #Render
    def render(self):
        #state renders
        self.state.render()
        
        #updates the display
        pygame.display.update()
        
        

#Run the main loop
if "__main__" == __name__:
                
    manager = Manager()
    manager._run()

    