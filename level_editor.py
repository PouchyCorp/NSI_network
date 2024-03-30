import pygame

pygame.init()

WIN = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("TAGLIATELE Level Editor")
grid = pygame.image.load('background.jpg')
rects = []

def wall(x1,y1,x2,y2):
    if x2 > x1 and y2 > y1:
        return pygame.Rect(x1,y1,(x2-x1),(y2-y1))
    
    
def draw():
    WIN.blit(grid,WIN.get_rect())
    for rect in rects:
        pygame.draw.rect(WIN,"red",rect)
    pygame.display.update()

running = True

clic = 1
xy_1, xy_2 = (), ()
    
while running :
    draw()
    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_type = event.button

            if clic == 1 :
                x1,y1 = event.pos
                clic = 2
            elif clic == 2 :
                x2,y2 = event.pos
                clic = 1
                if wall(x1,y1,x2,y2):
                    rects.append(wall(x1,y1,x2,y2))
            
            
    pygame.display.update()