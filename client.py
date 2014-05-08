from network import Handler
from network_connector import NetworkConnector, start_thread
from player import Player

players = {} # map player name to rectangle
myname = None
class Client(Handler, NetworkConnector):

    
    def on_close(self):
        #send msg to the server 'quit'
        print "****** Disconnected from server ******"
    '''on_msg() receives messages from the server
    for each message (except quit) it checks to see if the message sent from the server was a 
        command that was sent by you
    if the command (the player pressing the 'left' key) was sent by you, (you pressed the key)
        ignore it
    if it is from another player, either add/remove that player from the list of players, or 
        render/ do the action for that player within your own game state
    '''
    def on_msg(self, msg):
        global players, myname
        #sys.stdout.flush()
        if msg['msg_type'] == 'join':
            if myname == msg['their_name']:
                pass
            else:
                players[msg['their_name']] = Player(msg['their_name'])
                
        elif msg['msg_type'] == 'quit':
            del players[msg['their_name']]
            
        elif msg['msg_type'] == 'input':
            if myname == msg['their_name']:
                pass
            else:
                players[msg['their_name']].update(msg['input'])
        
        elif msg['msg_type'] == 'shot':
            if myname == msg['their_name']:
                pass
            else:
                players[msg['their_name']].update(shoot)
        
    def send_msg(self, msg):
        self.do_send(msg)       
'''
        if 'join' in msg:
            self.notify('player_joined', msg['join'], msg['topleft'])
        elif 'direction' in msg:
            self.notify('invaders_changed_direction', msg['invaders_changed_direction'], msg['new_direction'])
        elif 'left' in msg:
            self.notify('player_hit_left', msg['left'], msg['new_direction'])
        elif 'right' in msg:
            self.notify('player_hit_right', msg['right'], msg['new_direction'])
        elif 'shot' in msg:
            self.notify('invader took a shot', msg['invaders_shoot'])
        print msg
  '''  
    

'''Starts the client connection'''                            
def start_client():
    host, port = 'localhost', 8888
    client = Client(host, port)
    #client.do_send({'join':'JOINED!'})

    start_thread()
    
    return client
    
    