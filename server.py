from network import Handler, poll, Listener, get_my_ip
#from threading import Thread, Lock

 
handlers = {}  # map client handler to user name
server = None

def get_server():
    return server

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
        server_listener = self.server_listener
        if 'join' in msg:
            server_listener.player_joined(handlers[handler], msg['join'])
        elif 'player_performed_action' in msg:
            server_listener.player_performed_action(msg['player_performed_action'], msg['action'])
            #self.send_msg(msg)
        elif 'invaders_hit' in msg:
            server_listener.invaders_hit(msg['invaders_hit'], msg['wave_number'], msg['invader_number'])
        elif 'quit' in msg:
            handler.do_send({'quit':handlers[handler]})
            self.server_listener.player_left(handlers[handler])
        #print msg
    
    def send_msg(self, msg, client_id = 0):
        #if handlers.__len__()>0:
        if client_id:
            self._send_to_id(msg, client_id)
        else:
            self._send_to_all_users(msg)

    def _send_to_id(self, msg, client_id):
        for h in handlers:
            if handlers[h] == client_id:
                h.do_send(msg)

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
    
    def player_joined(self, player_id, x_pos): pass
    def player_left(self, player_id): pass
    def player_performed_action(self, player_id, action): pass
    
    def invaders_hit(self, player_id, wave_number, invader_number): pass
    