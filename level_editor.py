import pygame

pygame.init()

WIN = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("TAGLIATELE Level Editor")
grid = pygame.image.load('background.jpg')
rects = []

def wall(x1,y1,x2,y2):
    if x2 > x1 and y2 > y1:
        return pygame.Rect(x1,y1,abs(x2-x1),abs(y2-y1))
    elif x2 > x1 and y2 < y1:
        return pygame.Rect(x1,y2,abs(x2-x1),abs(y2-y1))
    elif x2 < x1 and y2 > y1 :
        return pygame.Rect(x2,y1,abs(x2-x1),abs(y2-y1))
    elif x2 < x1 and y2 < y1 :
        return pygame.Rect(x2,y2,abs(x2-x1),abs(y2-y1))
    
def draw():
    WIN.blit(grid,WIN.get_rect())
    for rect in rects:
        pygame.draw.rect(WIN,"red",rect)
    pygame.display.update()

running = True

clicked = False
xy_1, xy_2 = (), ()
    
while running :
    draw()
    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_type = event.button

            if clicked == False :
                x1,y1 = event.pos
                clicked = True
            elif clicked == True :
                x2,y2 = event.pos
                clicked = False
                rects.append(wall(x1,y1,x2,y2))
            
            
    pygame.display.update()
