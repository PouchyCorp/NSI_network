import pygame as pg

class Player():
    def __init__(self,x,y,num):
        self.x = x
        self.y = y
        self.num = num
        self.rect = (x,y,20,20)

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= 1
        if keys[pg.K_RIGHT]:
            self.x += 1
        if keys[pg.K_DOWN]:
            self.y += 1
        if keys[pg.K_UP]:
            self.y -= 1
    def updateValues(self):
        self.rect = (self.x,self.y,20,20)
    