from network import Handler, poll
import sys
from threading import Thread


myname = raw_input('What is your name? ')

class Client(Handler):
    
    global myname
    
    def on_close(self):
        global running
        running = False
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg):
        if 'txt' in msg and msg['speak'] != myname:
            print msg['speak'] +": "+ msg['txt']
        elif 'joined' in msg:
            print msg['joined']+ " joined. Users: "+msg['users']
        elif 'left' in msg:
            print msg['left']+ " left the room. Users: "+msg['users']
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

running = True #running state
while running:
    mytxt = sys.stdin.readline().rstrip()
    client.do_send({'speak': myname, 'txt': mytxt})
