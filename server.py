from network import Handler, Listener
#from threading import Thread, Lock

from network_connector import NetworkConnector, start_thread
 
handlers = {}  # map client handler to user name
server = None

class ServerHandler(Handler):
    
    global handlers, server
    
    def on_open(self):
        handlers[self] = None
         
    def on_close(self):
        del handlers[self] #remove from the dictionary
     
    def on_msg(self, msg):
        #Keeps the handler ip
        if 'join' in msg:
            handlers[self] = msg['join']
            
        if server != None:
            server.on_msg(msg, self)

    

class Server(NetworkConnector):
    
    global handlers
    
    def on_msg(self, msg, handler):
        if 'join' in msg:
            self.notify('player_joined', msg['join'], msg['topleft'])
            self.send_msg(msg)
        elif 'performed_action' in msg:
            self.notify('player_performed_action', msg['performed_action'], msg['action'])
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
def start_server():
    global server
    
    port = 8888
    Listener(port, ServerHandler)
    server = Server()
    
    start_thread()
    
    return server
