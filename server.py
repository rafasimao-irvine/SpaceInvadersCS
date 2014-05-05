from network import Listener, Handler, poll

from threading import Thread
 
handlers = {}  # map client handler to user name

class ServerHandler(Handler):
    
    global handlers
    
    def on_open(self):
        handlers[self] = None
         
    def on_close(self):
        del handlers[self] #remove from the dictionary
     
    def on_msg(self, msg):
        print msg


    def _send_to_all_users(self,msg):
        for h in handlers:
            h.do_send(msg)


class ServerListener(object):
    
    def player_joined(self, player): pass
    def player_left(self, player): pass
    def player_performed_action(self, player, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_driection(self, new_direction): pass
    def invaders_shoot(self, new_projectile): pass



def periodic_poll():
    while 1:
        poll(timeout=0.05)  # seconds

def start_server():
    port = 8888
    server = Listener(port, ServerHandler)
    
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()

    return server
