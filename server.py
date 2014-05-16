from network import Handler, poll, Listener
#from threading import Thread, Lock

 
handlers = {}  # map client handler to user name
server = None

class ServerHandler(Handler):
    
    global handlers, server
    def on_open(self):
        handlers[self] = generate_id()
         
    def on_close(self):
        del handlers[self] #remove from the dictionary
     
    def on_msg(self, msg):
        #Keeps the handler ip
        if server != None:
            server.on_msg(msg, self)
            


_ids = 0
def generate_id():
    global _ids
    _ids += 1
    return _ids

    

class Server():
    
    global handlers
    server_listener = None
    def on_msg(self, msg, handler):
        if 'join' in msg:
            handler.do_send({'join':handlers[handler]})
            self.server_listener.player_joined(handlers[handler], msg['join'])
        #elif 'performed_action' in msg:
            #self.send_msg(msg)
        print msg
    
    def send_msg(self, msg):
        #if handlers.__len__()>0:
        self._send_to_all_users(msg)

    def _send_to_all_users(self, msg):
        #lock = Lock()
        #lock.acquire()
        for h in handlers:
            h.do_send(msg)
        #lock.release()


'''Starts the server connection'''
def start_server(server_listener):
    global server
    
    port = 8888
    Listener(port, ServerHandler)
    server = Server()
    
    server.server_listener = server_listener
    #start_thread()
    
    return server


'''Keep polling'''
def periodic_poll():
    poll(timeout=0.05)  # seconds
    
    
    
'''ServerListener abstract class, must be extended to receive a message at the network'''
class ServerListener(object):
    
    def player_joined(self, player_id, topleft): pass
    def player_left(self, player_ip): pass
    def player_performed_action(self, player_ip, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_direction(self, new_direction): pass
    def invaders_shoot(self, topleft): pass