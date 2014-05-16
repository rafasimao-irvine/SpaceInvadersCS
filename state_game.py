import pygame
from state import State
from random import randint
from input_listener import InputListener
from player import Player
from invaders_manager import InvadersManager
#from Invaders import Invaders

from client import get_client, ClientListener

'''
Main game state. Might be the class where the whole game will run at.
'''
class StateGame(State, InputListener, ClientListener):

    player = Player()
    #players_list = {}
    #invader = Invaders(0)
    invader_manager = InvadersManager()

    def __init__(self, screen, inputManager):
        State.__init__(self, screen, inputManager)
        inputManager.attach(self)
        
        #self.players_list[self.player] = networkConnector.my_ip
        
        self.board_bounds = pygame.Rect(0,0,screen.get_width(),screen.get_height())
        
        self.fontObj = pygame.font.Font('freesansbold.ttf', 22)
        
        
    def destroy(self):
        self.inputManager.detach(self)
            
    
    '''Update'''
    def update(self, dt):
        State.update(self, dt) 

        #Updates the game objects
        self.player.update(dt)
        #for player in self.players_list:
        #    player.update(dt)
        
        #self.invader.update(dt)
        self.invader_manager.update(dt)

        #treats projectiles hits        
        self._treat_invader_projectiles()
        self._treat_players_projectiles()
       
    ''' 
    'Make invaders projectiles collisions and perform the consequences'
    def _treat_invader_projectiles(self):
        if self.invader_manager.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in self.invader_manager.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(self.invader_manager.projectile_list, shot):
                    #If it collides with the player, the player receives the damage and the projectile is removed
                    if shot.is_colliding_with(self.player):
                        self.player.receive_hit()
                        self.invader_manager.projectile_list.remove(shot)

    'Make players projectiles collisions and perform the consequences'
    def _treat_players_projectiles(self):
        if self.player.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in self.player.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(self.player.projectile_list, shot):
                    collided = False
                    for invader in self.invader_manager.invaders_list:
                        if not collided and shot.is_colliding_with(invader):
                            self.player.projectile_list.remove(shot)
                            self.invader_manager.invaders_list.remove(invader)
                            self.player.increase_score(15)
                            #self.invader_manager.speedUp()
                            collided = True
    '''
    
    'Make invaders projectiles collisions and perform the consequences'
    def _treat_invader_projectiles(self):
        if self.invader_manager.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in self.invader_manager.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(self.invader_manager.projectile_list, shot):
                    #If it collides with the player, the player receives the damage and the projectile is removed
                    #collided = False
                    #for player in self.players_list:
                    if shot.is_colliding_with(self.player):
                        self.player.receive_hit()
                        #collided = True
                    #if collided:
                        self.invader_manager.projectile_list.remove(shot)

    'Make players projectiles collisions and perform the consequences'
    def _treat_players_projectiles(self):
        player = self.player
        #for player in self.players_list:
        if player.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in player.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(player.projectile_list, shot):
                    collided = False
                    for invader in self.invader_manager.invaders_list:
                        if not collided and shot.is_colliding_with(invader):
                            player.projectile_list.remove(shot)
                            self.invader_manager.invaders_list.remove(invader)
                            player.increase_score(15)
                            #self.invader_manager.speedUp()
                            collided = True                 
                    
    'Removes a projectile from a projectile list if it is out of the board bounds.' 
    'Returns True if it is removed and False if it is not.'
    def _remove_if_out_of_board(self, projectile_list, projectile):
        #If it is out of the board game box, it is removed
        if not self.board_bounds.colliderect(projectile.get_collision_box()):
            projectile_list.remove(projectile)
            return True
        
        return False
   

    
    '''Render'''
    def render(self):
        if self.player.life > 0:
            State.render(self) 
            #background
            self.screen.fill(pygame.Color(0,0,0))
        
            self.player.render(self.screen)
            #for player in self.players_list:
            #    player.render(self.screen)
            #self.invader.render(self.screen)
            self.invader_manager.render(self.screen)
            
            self.draw_player_score()
        elif self.player.life <= 0:
            self.draw_game_over_screen()
       
    'Draws the main player score' 
    def draw_player_score(self):
        msgSurfaceObject = self.fontObj.render("Score: "+str(self.player.score), False, pygame.Color(205,255,205))
        msgRectObject = msgSurfaceObject.get_rect()
        msgRectObject.topleft = (25, 25)

        self.screen.blit(msgSurfaceObject, msgRectObject)
        
    'Draws the game over screen'     
    def draw_game_over_screen(self):
        self.screen.fill(pygame.Color(0,0,0))
        
        msgSurfaceObject = self.fontObj.render("Game Over", False, pygame.Color(205,255,205))
        msgRectObject = msgSurfaceObject.get_rect()
        msgRectObject.topleft = (425, 300)

        self.screen.blit(msgSurfaceObject, msgRectObject)
        
        
      
    '''***** Input receiver: *****'''
      
    'Receives inputs and treats them if they corresponds to moving or firing'
    def receive_input(self, event):
        client = get_client()
        my_id = client.my_id
        #Starts moving
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.move_left(True)
                client.do_send({'performed_action':my_id, 'action':'keydown_left'})
            elif event.key == pygame.K_d:
                self.player.move_right(True)
                client.do_send({'performed_action':my_id, 'action':'keydown_right'})
        #Finishes moving
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.player.move_left(False)
                client.do_send({'performed_action':my_id, 'action':'keyup_left'})
            elif event.key == pygame.K_d:
                self.player.move_right(False)
                client.do_send({'performed_action':my_id, 'action':'keyup_right'})
        #Starts firing projectile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.fire_shot(True)
                client.do_send({'performed_action':my_id, 'action':'keydown_fire'})
        #Finishes firing projectile
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.player.fire_shot(False)
                client.do_send({'performed_action':my_id, 'action':'keyup_fire'})
    
    
        
    '''***** Network receivers: *****'''
    
    def player_joined(self, player_ip, topleft):
        ClientListener.player_joined(self, player_ip, topleft)
        
        player = Player()
        player.box.topleft = topleft
        player.color = pygame.Color(randint(80,200),randint(80,200),randint(80,200))
        
        #self.players_list[player] = player_ip
        
