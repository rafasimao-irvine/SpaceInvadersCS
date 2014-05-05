from network_connector import NetworkHandler, NetworkListener, start_thread

class Client(NetworkHandler):
    
    def on_close(self):
        print "****** Disconnected from server ******"
    
    def on_msg(self, msg): pass
    

'''Starts the client connection'''                            
def start_client():
    host, port = 'localhost', 8888
    client = Client(host, port)
    #client.do_send({'join':'JOINED!'})

    start_thread()
    
    return client
    
    