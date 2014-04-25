from network import Listener, Handler, poll

 
handlers = {}  # map client handler to user name
 
def get_users():
    output = "Users: "
    i = 0
    for user in handlers.keys():
        if i < len(handlers.keys()) - 1:
            output += user + ","
        else:
            output += user
        i += 1
    return output 
                
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        if "join" in msg:
            handlers[msg["join"]] = self
            for user in handlers.keys():
                handlers[user].do_send({"out" : msg["join"] + " joined. " + get_users()})
        elif "speak" in msg:
            for user in handlers.keys():
                if user != msg["speak"]:
                    handlers[user].do_send({"out" : msg["speak"] + ": " + msg["txt"]})
        elif "quit" in msg:
            del handlers[msg["quit"]]
            for user in handlers.keys():
                handlers[user].do_send({"out" : msg["quit"] + " left the room. " + get_users()}) 
        
port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds
    