from random import randint
from time import sleep
from common import Model

################### CONTROLLER #############################

import pygame
#from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

currPellet = None
pelletPos = None

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        cmd = None
        global pelletPos
        global currPellet
        if not(currPellet and pelletPos) or (currPellet[0] != self.m.pellets[pelletPos][0] or currPellet[1] != self.m.pellets[pelletPos][1]):
            pelletPos = randint(0,3)
            currPellet = [self.m.pellets[pelletPos][0], self.m.pellets[pelletPos][1]]
        b = self.m.mybox
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        if myrect.topleft[0] < currPellet[0]:
            cmd = 'right'
        elif myrect.topleft[1] < currPellet[1]:
            cmd = 'down'
        elif myrect.topleft[0] > currPellet[0]:
            cmd = 'left' 
        else:
            cmd = 'up'
            
        if cmd:
            self.m.do_cmd(cmd)

################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self, numFrames):
        #screen = self.screen
        #borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        #pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        b = self.m.mybox
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        #screen.fill((0, 0, 64))  # dark blue
        #pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue$
        #[pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        #[pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        if numFrames == 50:
            print "Position: " + str(myrect.x) + ", " + str(myrect.y)
        pygame.display.update()
        
    
################### LOOP #############################

model = Model()
c = Controller(model)
v = View(model)
numFrames = 0

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display(numFrames)
    if numFrames == 50:
        numFrames = 0
    numFrames += 1