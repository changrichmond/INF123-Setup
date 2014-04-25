from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')
running = True 

class Client(Handler):
    
    def on_close(self):
        global running
        running = False
        print "**** Disconnected from server ****"

    def on_msg(self, msg):
        print msg["out"]
        
host, port = "localhost", 8888
client = Client(host, port)
client.do_send({"join": myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while running:
    mytxt = sys.stdin.readline().rstrip()
    if mytxt == "quit":
        client.do_send({"quit" : myname })
        client.do_close()
    else:
        client.do_send({"speak": myname, "txt": mytxt})