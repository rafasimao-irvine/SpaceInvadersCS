from network import Listener

from network_connector import NetworkHandler, NetworkListener, start_thread
 
handlers = {}  # map client handler to user name

class ServerHandler(NetworkHandler):
    
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


def start_server():
    port = 8888
    server = Listener(port, ServerHandler)
    
    start_thread()

    return server
