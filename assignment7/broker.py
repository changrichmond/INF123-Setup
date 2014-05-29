from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        global names
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name] = self
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            toAll = True
            broadcastTo = []
            global subs
            for word in txt.split():
                if word.startswith("+"):
                    if not subs.has_key(word[1:]):
                        subs[word[1:]] = []
                    if not names[name] in subs[word[1:]]:
                        subs[word[1:]].append(names[name])
                    toAll = False
                elif word.startswith("#"):
                    if subs.has_key(word[1:]):
                        for h in subs[word[1:]]:
                            broadcastTo.append(h)
                    toAll = False
                elif word.startswith("-"):
                    if subs.has_key(word[1:]):
                        if (names[name] in subs[word[1:]]):
                            subs[word[1:]].remove(names[name])
                    toAll = False
                elif word.startswith("@"):
                    if names.has_key(word[1:]):
                        broadcastTo.append(names[word[1:]])
                    toAll = False
            if toAll:
                broadcast({'speak': name, 'txt': txt})
            else:
                for h in broadcastTo:
                    h.do_send({'speak': name, 'txt' : txt})


Listener(8888, MyHandler)
while 1:
    poll(0.05)
