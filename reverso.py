import pygame, classes
pygame.init()

RESOLUTION = [640,720]
windowTitle = "Reverso"
stopGame = False
background = ( 96,191, 77)
black = (  0,  0,  0)

screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True

    pygame.display.flip()

pygame.quit()
