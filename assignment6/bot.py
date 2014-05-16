from random import randint

################### CONTROLLER #############################

import pygame
from network import Handler, poll
from pygame import Rect
from pygame.display import set_mode, update as update_pygame_display
from pygame.draw import rect as draw_rect
from pygame.event import get as get_pygame_events
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame.time import Clock


borders = []
trackPellets = []
pellets = []
players = {}
myname = None
box = None

currPellet = None
pelletPos = None
clock = Clock()

def make_rect(quad):
    x, y, w, h = quad
    return Rect(x, y, w, h)

def pelletsChanged():
    global trackPellets, pellets
    for x in range(4):
        if trackPellets[x]: 
            if trackPellets[x][0] != pellets[x][0] or trackPellets[x][1] != pellets[x][1]:
                return True
    return False

class Client(Handler):
    
    def on_msg(self, data):
        global borders, trackPellets, pellets, players, myname, box
        borders = [make_rect(b) for b in data['borders']]
        trackPellets = pellets
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']
        box = players[myname]
    
    def on_open(self):
        print 'Connected to server'
    
    def on_close(self):
        print 'Disconnected from server'
        exit();
        
client = Client('localhost', 8888)
#valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right' }

class Controller():
    def __init__(self):
        pygame.init()
    
    def poll(self):
        cmd = None
        global pelletPos, currPellet
        global pellets, box
        if not(currPellet and pelletPos):
            pelletPos = randint(0,3)
            currPellet = [pellets[pelletPos][0], pellets[pelletPos][1], pellets[pelletPos][2], pellets[pelletPos][3]]
        if (currPellet[0] != pellets[pelletPos][0] or currPellet[1] != pellets[pelletPos][1]):
            pelletPos = randint(0,3)
            currPellet = [pellets[pelletPos][0], pellets[pelletPos][1], pellets[pelletPos][2], pellets[pelletPos][3]]
            print 'Pellet eaten'
#         if box.topleft[0] < currPellet[0] or  box.topleft[0] + 1 < currPellet[0]:
#             cmd = 'right'
#         elif box.topleft[1] < currPellet[1] or box.topleft[1] - 1  < currPellet[1]:
#             cmd = 'down'
#         elif box.topleft[0] > currPellet[0] or  box.topleft[0] + 1 > currPellet[0]:
#             cmd = 'left' 
#         else:
#             cmd = 'up'
        if currPellet[0] >= box[0]:
            cmd = 'right'
        elif currPellet[0] + currPellet[2] <= box[0]: # p[2] to avoid stuttering left-right movement
            cmd = 'left'
        elif currPellet[1] >= box[1]:
            cmd = 'down'
        else:
            cmd = 'up'
        return cmd
            
################### VIEW #############################

class View():
    def __init__(self):
        pygame.init()
#         self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        pass
#         global borders, pellets, box
#         screen = self.screen
#         screen.fill((0, 0, 64))  # dark blue
#         pygame.draw.rect(screen, (0, 191, 255), box)  # Deep Sky Blue$
#         [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
#         [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
#         if numFrames == 50:
#            #print "Position: " + str(box.x) + ", " + str(box.y)
#             print "Position: " + str(box[0]) + ", " + str(box[1]) + " Pellet: " + str(currPellet[0]) + ", " + str(currPellet[1])
#         pygame.display.update()
        
    
################### LOOP #############################

c = Controller()
v = View()
# numFrames = 0

while 1:
    poll()
    
    for event in get_pygame_events():
        if event.type == QUIT:
            exit()
            
    move = c.poll()
    if move:
        msg = {'input': move }
        client.do_send(msg)
#     v.display()
#     if numFrames == 50:
#         numFrames = 0
#     numFrames += 1
    clock.tick(50)