from network import Handler, poll
from threading import Thread

class NetworkHandler(Handler):
    _observers = []
    
    'Used to add one object to the list of observers'
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    'Used to take one object off the list of observers'
    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
        

class NetworkListener(object):
    
    def player_joined(self, player): pass
    def player_left(self, player): pass
    def player_performed_action(self, player, action): pass
    
    def player_new_score(self, score): pass

    def invaders_changed_driection(self, new_direction): pass
    def invaders_shoot(self, new_projectile): pass

        
def periodic_poll():
    while 1:
        poll(timeout=0.05)  # seconds

        
def start_thread():
    thread = Thread(target=periodic_poll)
    thread.daemon = True  # die when the main thread dies 
    thread.start()
    
    