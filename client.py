from network import Handler, poll, get_my_ip
from threading import Thread

client = None

class Client(Handler):
    
    client_listener = None
    connected = False
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
        print msg
    

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
    
    def player_joined(self, player_ip, topleft): pass
    def player_left(self, player_ip): pass
    def player_performed_action(self, player_ip, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_direction(self, new_direction): pass
    def invaders_shoot(self, topleft): pass
