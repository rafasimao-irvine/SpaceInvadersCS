from network import poll, get_my_ip
from threading import Thread

'''
class NetworkMessages(object):    
    #main messages
    JOIN = 'join'
    LEFT = 'left'
    PERFORMED_ACTION = 'perormed_action'
    NEW_SCORE = 'new_score'
    INVADERS_CHANGED_DIRECTION = 'invaders_changed_direction'
    INVADERS_SHOOT = 'invaders_shoot'
    
    #args
    ARG_TOPLEFT = 'topleft'
    ARG_SCORE = 'score'
    ARG_ACTION = 'action'
    ARG_DIRECTION = 'new_direction'
    ARG_IP = 'ip'
'''

'''Used to attach the network listeners to the handler,
so that it can notify them when something happens'''
class NetworkConnector(object):

    #Gets the local ip
    my_ip = get_my_ip()
    _networkListeners = []
    
    'Used to add one object to the list of observers'
    def attach(self, networkListeners):
        if not networkListeners in self._networkListeners:
            self._networkListeners.append(networkListeners)

    'Used to take one object off the list of observers'
    def detach(self, networkListener):
        try:
            self._networkListeners.remove(networkListener)
        except ValueError:
            pass
        
        
    'Notifies the observers that the following event happened'
    def notify(self, method_name, *args):
        for networkListener in self._networkListeners:
            method = getattr(networkListener, method_name)
            method(*args)
    
    
    'Must be defined by the subclass. Used to send a message to someone'
    def send_msg(self, msg): pass
        
        
'''NetworkListener abstract class, must be extended to receive a message at the network'''
class NetworkListener(object):
    
    def player_joined(self, player_ip, topleft): pass
    def player_left(self, player_ip): pass
    def player_performed_action(self, player_ip, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_direction(self, new_direction): pass
    def invaders_shoot(self, topleft): pass

        
'''Keep polling'''
def periodic_poll():
    while 1:
        poll(timeout=0.05)  # seconds
        
'''Starts a new thread that will be continually polling to receive messages'''
def start_thread():
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
    
    