from network import Handler, poll
from player import Player
from threading import Thread
from time import sleep

event_queue = []
players = {} # map player name to rectangle
myname = None
keep_going = True
class Client(Handler):

    '''player_event() receives a msg from the Player class, and figures out what kind of msg to 
    send to the server
    '''
    def player_event(self, msg):
        if msg == "left":
            event_queue.append('left')
        elif msg == "right":
            event_queue.append('right')
        elif msg == "stop":
            event_queue.append('stop')
        elif msg == "shot":
            event_queue.append('shot')
        elif msg == "stop shot":
            event_queue.append('stop_shot')
        
    def on_close(self):
        #send msg to the server 'quit'
        print "****** Disconnected from server ******"
        
        
    '''on_msg() receives messages from the server
    for each message (except quit) it checks to see if the message sent from the server was a 
        command that was sent by you
    if the command (the player pressing the 'left' key) was sent by you, (you pressed the key)
        ignore it
    if it is from another player, either add/remove that player from the list of players, or 
        render/ do the action for that player within your own game state
    '''
    def on_msg(self, msg):
        global players, myname
        #sys.stdout.flush()
        if msg['msg_type'] == 'join':
            if myname == msg['their_name']:
                for p in msg['players_list']:
                    players[p.name] = Player(p.name)
            else:
                players[msg['their_name']] = Player(msg['their_name'])
                
        elif msg['msg_type'] == 'quit':
            del players[msg['their_name']]
            
        elif msg['msg_type'] == 'input':
            if myname == msg['their_name']:
                pass
            else:
                players[msg['their_name']].update(msg['input'])
        
        elif msg['msg_type'] == 'shot':
            if myname == msg['their_name']:
                pass
            else:
                players[msg['their_name']].fire_shot(True)
     
    
def process_input(message):
        msg = message
        if msg == 'quit' or msg == 'exit':
            client.do_close()
        elif msg: # ignore empty strings
            client.do_send({'myname': myname, 'input': msg})
    
'''Starts the client connection'''
thread= None
global client

def start_client():            
    host, port = 'localhost', 8888
    global client
    client = Client(host, port)
    #client.do_send({'join':'JOINED!'})

    thread = Thread(target=process_input)
    thread.daemon = True # die when the main thread dies
    thread.start()
    client.do_send('join')
    return client

'''run the client
'''    
def run():
    while 1:
    
        poll() # push and pull network messages

        for m in event_queue:
            process_input(m) 
        event_queue = []
        sleep(1. / 20) # seconds