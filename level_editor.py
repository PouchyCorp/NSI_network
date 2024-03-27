import pygame

pygame.init()

WIN = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("TAGLIATELE Level Editor")
grid = pygame.image.load('background.jpg')

def wall(xy_1,xy_2):
    WIN.blit(grid,WIN.get_rect())
    
    X = xy_1[0] - xy_2[0]
    Y = xy_1[1] - xy_2[1]
    x, y, w, h = 0, 0, 0, 0
    
    if X < 0 and Y > 0 :
        x, y, w, h = xy_1[0], xy_1[1], xy_1[0] - xy_2[0], xy_1[1] - xy_2[1]
    elif X < 0 and Y < 0 :
        x, y, w, h = xy_1[0], xy_1[1], - (xy_1[0] - xy_2[0]), - (xy_1[1] - xy_2[1])
    elif X > 0 and Y > 0 :
        x, y, w, h = xy_2[0], xy_2[1], xy_1[0] - xy_2[0], xy_1[1] - xy_2[1]
    elif X > 0 and Y < 0 :
        x, y, w, h = xy_2[0], xy_2[1], - (xy_1[0] - xy_2[0]), - (xy_1[1] - xy_2[1])
    print(x, y, w, h)
    pygame.draw.rect(WIN,"red",pygame.Rect(x, y, w, h))
    pygame.display.update()

running = True

clic = 1
xy_1, xy_2 = (), ()
    
while running :

    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_type = event.button
            if clic == 1 :
                xy_1 += event.pos
                clic = 2
                print(xy_1)
            elif clic == 2 :
                xy_2 += event.pos
                clic = 1
                print(xy_2)
                wall(xy_1,xy_2)
                xy_1, xy_2 = (), ()
            
            
    pygame.display.update()