from network import Handler, poll, get_my_ip
from threading import Thread

client = None

def get_client():
    return client

class Client(Handler):
    
    client_listener = None
    connected = False
    died = False
    sent = False
    my_id = 0
    my_ip = get_my_ip()
    def on_open(self):
        self.connected = True
        print "****** Connected to the server ******"
    
    def on_close(self):
        self.connected = False
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg):
        if 'join' in msg:
            self.my_id = msg['join']
            self.client_listener.joined(msg['join'])
        elif 'player_joined' in msg:
            self.client_listener.player_joined(msg['player_joined'], msg['topleft'])
        elif 'quit' in msg:
            self.client_listener.player_left(msg['quit'])
        elif 'player_performed_action' in msg:
            self.client_listener.player_performed_action(msg['player_performed_action'], msg['action'])
        elif 'invaders_changed_direction' in msg:
            self.client_listener.invaders_changed_direction(
                                       msg['invaders_changed_direction'], 
                                       msg['position'], msg['how_many_moves'])
        elif 'invaders_shoot' in msg:
            self.client_listener.invaders_shoot(msg['invaders_shoot'])
        elif 'invaders_died' in msg:
            self.client_listener.invaders_died(msg['invaders_died'])
        elif 'invaders_hit_response' in msg:
            self.client_listener.invaders_hit_response(msg['invaders_hit_response'], msg['score'])
            
        #print msg
    

'''Starts the client connection'''                            
def start_client(client_listener):
    global client
    
    host, port = 'localhost', 8888
    client = Client(host, port)
    client.client_listener = client_listener
        
    #client.do_send({'join':'JOINED!'})

    #start_thread()
    
    return client

'''Keep polling'''
def periodic_poll():
    poll(timeout=0.05)  # seconds

    
'''Starts a new thread that will be continually polling to receive messages'''
def start_thread():
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
    
    
'''ClientListener abstract class, must be extended to receive a message'''
class ClientListener(object):
    
    def joined(self, player_id): pass
    
    def player_joined(self, player_id, topleft): pass
    def player_left(self, player_id): pass
    def player_performed_action(self, player_id, action): pass
    
    def invaders_hit_response(self, invader, score): pass
    def invaders_died(self, invader): pass
    def invaders_changed_direction(self, new_direction, invaders_position, how_many_moves): pass
    def invaders_shoot(self, projectile): pass
