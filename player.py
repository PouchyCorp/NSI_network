import pygame as p
from bullet import Bullet
class Player():
    def __init__(self,x,y,num):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.num = num
        self.rect = (x,y,self.w,self.h)
        self.mouseDir = p.Vector2(0,0)
        self.pos = (self.x,self.y)
        self.shootedBullets : list[Bullet] = []

    def move(self):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            self.x -= 3
        if keys[p.K_RIGHT]:
            self.x += 3
        if keys[p.K_DOWN]:
            self.y += 3
        if keys[p.K_UP]:
            self.y -= 3

    def updateValues(self):
        self.pos = (self.x,self.y)
        self.rect = (self.x,self.y,self.w,self.h)
        self.mouseDir = p.math.Vector2(p.mouse.get_pos()[0]- self.x,
                                        p.mouse.get_pos()[1] - self.y)
        if self.mouseDir == p.Vector2(0,0):
            print('u tried lol')
            self.mouseDir = p.Vector2(0,-1)
        self.mouseDir.scale_to_length(20)
        
    