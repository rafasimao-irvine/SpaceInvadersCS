from network import Handler, poll
from threading import Thread

class Client(Handler):
    
    def on_close(self):
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg): pass
    
    
class ClientListener(object):
    
    def player_joined(self, player): pass
    def player_left(self, player): pass
    def player_performed_action(self, player, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_driection(self, new_direction): pass
    def invaders_shoot(self, new_projectile): pass

    
def periodic_poll():
    while 1:
        poll(0.05)  # seconds
    
                            
def start_client():
    host, port = 'localhost', 8888
    client = Client(host, port)
    client.do_send({'join':'JOINED!'})

    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
    
    return client
    
    