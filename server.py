from network import Handler, Listener, poll
from time import sleep
from player import Player
 
handlers = {}  # map client handler to user name
server = None
players = {} # map a client handler to a player object
player_id = 0
global event_queue

def broadcast(msg):
    global players
    #[h.do_send(msg) for h in players.keys()]
    for h in handlers.keys():
        h.do_send(msg)


def generate_name():
    global player_id
    player_id += 1
    return str(player_id)
    
# map inputs received from clients to directions
input_dir = {'left': [-1, 0], 'right': [1, 0]}


class Server(Handler):
    '''on_open() is called whenever a client connects, so a join msg is going to be sent
    on_close() is called whenever a client disconnects, so a quit msg is going to be sent
    on_msg() is called in every other case
    '''
    def on_open(self):
        #event_queue.append(('join', self))
        player_name = generate_name()
        players[self] = Player(player_name)
        msg = {'msg_type': 'join',
                'their_name': players[self].name,
                'players_list': players
               }
        broadcast(msg)
              
    def on_close(self):
        #event_queue.append(('quit', self))
        msg = {'msg_type':'quit',
               'their_name': players[self].name,
              }
        del players[self]
        broadcast(msg)
     
    def on_msg(self, msg):
        #event_queue.append((msg['input'], self))
        print "msg" + msg
        '''
        if msg == 'quit':
                msg = {'msg_type':'quit',
                       'their_name': players[handler].name(),
                       }
                del players[handler]
                broadcast(msg)
        '''
        if msg == 'join':
                player_name = generate_name()
                players[self] = Player(player_name)
                msg = {'msg_type': 'join',
                       'their_name': players[self].name(),
                       'players_list': players
                       }
                broadcast(msg)
        ''' 
        elif msg == 'input':
                msg = {'msg_type': 'player_movement',
                         'their_name': players[handler].name(),
                         'input': event
                         }
                broadcast(msg)
        
        elif msg == 'shot':
                msg = {'msg_type':
        '''

'''Starts the server connection'''
def start_server():
    global server
    
    event_queue = [] # list of ('event', handler)
    
    port = 8888
    server = Listener(port, Server)
    #server = Server()
    
    #start_thread()
    
    return server
'''main loop for server functionality, poll
1) poll to check for players' actions
2) send out msgs to clients based on the events that were put into event_queue (
'''
def run():

    #while 1:
    
        # enqueue the player events received by the client handlers
        poll()
        
        '''checks what kind of event happened, then filters it so that it can send the correct
        event out to the clients.
    
        within the messages, the first part is the type of message(player joined, player quit
            player pushed a key, etc)
        the second part is the name of the player that did that event
        '''
        '''
        for event, handler in event_queue:
            if event == 'quit':
                msg = {'msg_type':'quit',
                       'their_name': players[handler].name(),
                       }
                del players[handler]
                broadcast(msg)
                
            elif event == 'join':
                player_name = generate_name()
                players[handler] = Player(player_name)
                msg = {'msg_type': 'join',
                       'their_name': players[handler].name(),
                       'players_list': players
                       }
                broadcast(msg)
            
            elif event == 'input':
                msg = {'msg_type': 'player_movement',
                         'their_name': players[handler].name(),
                         'input': event
                         }
                broadcast(msg)
        
            elif event == 'shot':
                msg = {'msg_type': 'player_shot',
                       'their_name': players[handler].name()
                      }
                broadcast(msg)
        '''
        event_queue = []
    
        sleep(1. / 20) # seconds

