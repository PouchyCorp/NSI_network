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
        self.lifeTime = 20
        self.noCollisionTime = 8
        
    def updateValues(self):
        self.x, self.y = (self.rect.x,self.rect.y)
        self.pos = (self.rect.x,self.rect.y)
        self.noCollisionTime -= 1
    

    def move(self, colliders, shields):
        shadowRect = self.rect.copy()
        shadowRect.move_ip(self.dir)
        shieldsCollider = [shield[1] for shield in shields.values()]
        allColliders = colliders + shieldsCollider
        collisions = shadowRect.collidelistall(allColliders)
        for collision in collisions:
            if shadowRect.collidelistall(shieldsCollider):
                print('pok')
            if self.lifeTime == 0:
                return
            self.lifeTime -= 1
            collider = allColliders[collision]
            if collider.top < self.rect.centery < collider.bottom:
                self.dir.x *= -1
            else:
                self.dir.y *= -1

            #fonction recursive oueeeee (pour que la balle ne traverse pas les murs)
            self.dir.scale_to_length(self.speed)
            p.Rect.move_ip(self.rect,self.dir)
            #if self.rect.collidelistall(allColliders):
            #    self.lifeTime = 0
            #    print('bonk')
            return

        self.dir.scale_to_length(self.speed)
        p.Rect.move_ip(self.rect,self.dir)
            