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


def periodic_poll():
    while 1:
        poll(timeout=0.05)  # seconds

def start_server():
    port = 8888
    Listener(port, ServerHandler)
    #server = Listener(port, MyHandler)
    
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
