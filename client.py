from network import Handler, poll
#import sys
from threading import Thread

#myname = raw_input('What is your name? ')

class Client(Handler):
    
    global myname
    
    def on_close(self):
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg): pass
    
    

def periodic_poll():
    while 1:
        poll(0.05)  # seconds
                            
def start_client():
    host, port = 'localhost', 8888
    #Client(host, port)
    client = Client(host, port)
    client.do_send({'join':'JOINED!'})

    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()