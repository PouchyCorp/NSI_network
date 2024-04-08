import pygame as p
class Bullet():
    def __init__(self,x,y,dir):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.dir = dir
        self.speed = 5
        self.pos = (self.x,self.y)
        self.rect : p.Rect = p.Rect(self.x,self.y,self.w,self.h)
        
    def updateValues(self):
        self.x, self.y = (self.rect.x,self.rect.y)
        self.pos = (self.rect.x,self.rect.y)

    def move(self):
        p.Rect.move_ip(self.rect,self.dir[0],self.dir[1])