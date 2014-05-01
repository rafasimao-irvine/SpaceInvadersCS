import sys
import pygame

'''
Class used to manager the inputs.
A class which wants to receive inputs must be a InputListener and
be attached to this class. Once a class attached to this wants to stop
receiving events it must be detached.
'''
class InputManager(object):

    def __init__(self):
        self._observers = []
    
    'Updates the amount of input events received'
    def update(self):
        for event in pygame.event.get():
            #Quit system
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.notify(event)
        
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
        
    'Notifies the observers that the following event happened'
    def notify(self, event):
        for observer in self._observers:
            observer.receive_input(event)