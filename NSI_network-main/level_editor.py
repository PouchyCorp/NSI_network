import pygame

pygame.init()

WIN = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("TAGLIATELE Level Editor")
grid = pygame.image.load('background.jpg')
rects = []

def walls(x1,y1,x2,y2):
    try :
        if x2 > x1 and y2 > y1:
            return pygame.Rect(x1,y1,abs(x2-x1),abs(y2-y1))
        elif x2 > x1 and y2 < y1:
            return pygame.Rect(x1,y2,abs(x2-x1),abs(y2-y1))
        elif x2 < x1 and y2 > y1 :
            return pygame.Rect(x2,y1,abs(x2-x1),abs(y2-y1))
        elif x2 < x1 and y2 < y1 :
            return pygame.Rect(x2,y2,abs(x2-x1),abs(y2-y1))
    except :
        return False

    
def draw(color):
    WIN.blit(grid,WIN.get_rect())
    for rect in rects:
        if rect:
            pygame.draw.rect(WIN,rect["color"],rect["wall"])
    pygame.display.update()

running = True
clicked = False
color = ""

while running :

    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            running = False
            
            break
            
        if event.type == pygame.MOUSEBUTTONDOWN:

            if clicked == False :
                x1,y1 = event.pos
                clicked = True
                button_type = event.button
            elif clicked == True :
                x2,y2 = event.pos
                clicked = False
                if button_type == 1:
                    color = "red"
                elif button_type == 3:
                    color = "blue"
                rects.append({"wall" : walls(x1,y1,x2,y2), "color" : color})
    

    draw(color)
         
