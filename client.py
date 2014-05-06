from network import Handler
from network_connector import NetworkConnector, start_thread

class Client(Handler, NetworkConnector):
    
    connected = False
    
    def on_open(self):
        self.connected = True
    
    def on_close(self):
        self.connected = False
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg):
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
    
    def send_msg(self, msg):
        self.do_send(msg)
    

'''Starts the client connection'''                            
def start_client():
    host, port = 'localhost', 8888
    client = Client(host, port)
    #client.do_send({'join':'JOINED!'})

    start_thread()
    
    return client
    
    