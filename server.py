from network import Listener, Handler, poll

 
handlers = {}  # map client handler to user name

class MyHandler(Handler):
    
    global handlers
    
    def on_open(self):
        handlers[self] = None
         
    def on_close(self):
        del handlers[self] #remove from the dictionary
     
    def on_msg(self, msg):

        message = "" # message that will be sent back
    
        # Joining the room
        if 'join' in msg:
            handlers[self] = msg['join'] #put the user in the dictionary
            # tell clients that someone joined
            message = {'joined' : msg['join'], 'users' : self._get_all_users()}
        
        # Txt msg
        else:
            # Leaving the room
            if msg['txt'] == "quit":
                self.do_close()
                # tell the others he left
                message = {'left':msg['speak'], 'users' : self._get_all_users()}

            else:
                message = msg # send it back
    
        if message != "":
            self._send_to_all_users(message)
        #print msg


    def _send_to_all_users(self,msg):
        for h in handlers:
            h.do_send(msg)

    def _get_all_users(self):
        users = ""
        for h in handlers:
            users = handlers[h] if users == "" else users +","+handlers[h]
        return users
 


port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds