import pygame as p
class Bullet():
    def __init__(self,x,y,dir):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.dir : p.Vector2 = dir
        self.speed = 7
        self.pos = (self.x,self.y)
        self.rect : p.Rect = p.Rect(self.x,self.y,self.w,self.h)
        self.lifeTime = 10
        self.noCollisionTime = 3
        
    def updateValues(self):
        self.x, self.y = (self.rect.x,self.rect.y)
        self.pos = (self.rect.x,self.rect.y)
        self.noCollisionTime -= 1

    def move(self, colliders : list[p.Rect]):
        shadowRect = self.rect.copy()
        shadowRect.move_ip(self.dir)
        if shadowRect.collidelistall(colliders):
            self.lifeTime -= 1
            if self.lifeTime == 0:
                return
            collider = colliders[shadowRect.collidelist(colliders)]
            #print(collider.top, self.rect.centery, collider.bottom )
            if collider.top < self.rect.centery < collider.bottom:
                self.dir.x *= -1
            else:
                self.dir.y *= -1
        self.dir.scale_to_length(self.speed)
        p.Rect.move_ip(self.rect,self.dir)
            