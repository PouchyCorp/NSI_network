import pygame as p
from bullet import Bullet
class Player():
    def __init__(self,x,y,num):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.num = num
        self.hp = 10
        self.rect : p.Rect = p.Rect(self.x,self.y,self.w,self.h)
        self.dir : p.Vector2 = p.Vector2(0,0)
        self.speed = 5
        self.mouseDir = p.Vector2(0,0)
        self.pos = (self.x,self.y)
        self.shootedBullets : list[Bullet] = []

    def recordInputDir(self) -> p.Vector2:
        keys = p.key.get_pressed()
        vector = p.Vector2(0,0)
        if keys[p.K_LEFT]:
            vector += (-self.speed,0)
        if keys[p.K_RIGHT]:
            vector += (self.speed,0)
        if keys[p.K_DOWN]:
            vector += (0,self.speed)
        if keys[p.K_UP]:
            vector += (0,-self.speed)
        return vector

    def move(self,dir : p.Vector2,colliders):
        if dir != p.Vector2(0,0):
            shadowRect = self.rect.copy()
            shadowRect.move_ip(dir)
            if shadowRect.collidelistall(colliders):
                #all that to 'glide' when moving in diagonal on a wall
                if dir.x == 0 or dir.y == 0:
                    return
                else:
                    shadowRect = self.rect.copy()
                    shadowRect.move_ip(dir.x,0)
                    if not shadowRect.collidelistall(colliders):
                        self.rect.move_ip((dir.x,0))
                        return
                    shadowRect = self.rect.copy()
                    shadowRect.move_ip(0,dir.y)
                    if not shadowRect.collidelistall(colliders):
                        self.rect.move_ip((0,dir.y))
                        return
                        
            else:
                self.rect.move_ip(dir)
        
        
        

    def updateValues(self):
        self.x, self.y = (self.rect.x,self.rect.y)
        self.pos = (self.rect.x,self.rect.y)
        #
        self.mouseDir = p.math.Vector2(p.mouse.get_pos()[0]- self.x,
                                        p.mouse.get_pos()[1] - self.y)
        if self.mouseDir == p.Vector2(0,0):
            print('u tried lol')
            self.mouseDir = p.Vector2(0,-1)
        self.mouseDir.scale_to_length(20)
        #

        
    