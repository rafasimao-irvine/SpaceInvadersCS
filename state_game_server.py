import pygame
from state import State
from player import Player
from invaders_manager import InvadersManager
#from Invaders import Invaders

from server import ServerListener, get_server

'''
Main game state. Might be the class where the whole game will run at.
'''
class StateGameServer(State, ServerListener):

    #Game started check
    game_started = False
    
    #List of players
    players_list = {}
    #invader = Invaders(0)
    invader_manager = InvadersManager()
    
    frame_counter = 0

    def __init__(self, screen, inputManager):
        State.__init__(self, screen, inputManager)
        
        self.board_bounds = pygame.Rect(0,0,screen.get_width(),screen.get_height())
        
        self.fontObj = pygame.font.Font('freesansbold.ttf', 22)
        
        
    def destroy(self):
        pass
    
    
    '''Update'''
    def update(self, dt):
        if self.game_started == True:
            if self.players_list.__len__() > 0:
                State.update(self, dt) 

                #Updates the game objects
                for player in self.players_list:
                    player.update(dt)
                #self.invader.update(dt)
                self.invader_manager.update(dt)

                #treats projectiles hits        
                self._treat_invader_projectiles()
                self._treat_players_projectiles()
        
    'Make invaders projectiles collisions and perform the consequences'
    def _treat_invader_projectiles(self):
        if self.invader_manager.projectile_list.__len__() > 0: 
            #Goes through all the invaders projectiles
            for shot in self.invader_manager.projectile_list:
                #If it is out of the board game box, it is removed
                if not self._remove_if_out_of_board(self.invader_manager.projectile_list, shot):
                    #If it collides with the player, the player receives the damage and the projectile is removed
                    collided = False
                    for player in self.players_list:
                        if shot.is_colliding_with(player):
                            player.receive_hit()
                            collided = True
                    if collided:
                        self.invader_manager.projectile_list.remove(shot)

    'Make players projectiles collisions and perform the consequences'
    def _treat_players_projectiles(self):
        for player in self.players_list:
            if player.projectile_list.__len__() > 0: 
                #Goes through all the invaders projectiles
                for shot in player.projectile_list:
                    #If it is out of the board game box, it is removed
                    if not self._remove_if_out_of_board(player.projectile_list, shot):
                        collided = False
                        for invader in self.invader_manager.invaders_list:
                            if not collided and shot.is_colliding_with(invader):
                                player.projectile_list.remove(shot)
                                player.increase_score(15)
                                #self.invader_manager.speedUp()
                                collided = True
                                
                                #send to the client
                                server = get_server()
                                if server:
                                    server.send_msg(
                                            {'invaders_died':self.invader_manager.invaders_list.index(invader), 
                                            'score':player.score}, self.players_list[player])
                                #then removes the invader
                                self.invader_manager.invaders_list.remove(invader)
                    
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
        State.render(self) 
        #background
        self.screen.fill(pygame.Color(0,0,0))
        
        #render objects
        for player in self.players_list:
            player.render(self.screen)
        self.invader_manager.render(self.screen)
        
    
    '''***** Network receivers: *****'''
    
    def player_joined(self, player_id, topleft):
        ServerListener.player_joined(self, player_id, topleft)
        
        player = Player()
        player.box.topleft = topleft
        self.players_list[player] = player_id
        
        self.game_started = True
        
        # send messages to the others
        server = get_server()
        
        server.send_msg({'join':player_id}, player_id)
        server.send_msg({'player_joined': player_id, 'topleft': topleft})
        #print "player_joined: "+str(player_ip)+" - "+str(topleft)
        
        
    def player_performed_action(self, player_id, action):
        print str(player_id)
        
        player = None
        for p in self.players_list:
            if self.players_list[p] == player_id:
                player = p
                
        if player != None:
            if action == 'keydown_left':
                player.move_left(True)
            elif action == 'keydown_right':
                player.move_right(True)
            elif action == 'keydown_fire':
                player.fire_shot(True)
            elif action == 'keyup_left':
                player.move_left(False)
            elif action == 'keyup_right':
                player.move_right(False)
            elif action == 'keyup_fire':
                player.fire_shot(False)
