import pygame, classes, os
pygame.init()

RESOLUTION = [640,720]
windowTitle = "Reverso"
stopGame = False
backgroundColour = ( 96,191, 77)
black = (  0,  0,  0)
SQUARE_SIZE = 80
BOARD_SIZE = 8
TOP_OFFSET = 40
RIGHT_OFFSET = 1

pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
background = pygame.image.load(os.path.join("sprites", "gameBoard.png")).convert()
pygame.display.get_surface().blit(background, (0,0))

def set_up_board(screen):
    newGroup = pygame.sprite.Group()
    newBoard = [None for i in range(BOARD_SIZE**2)]
    # Use i = x + wy where i is the desired index in the 1D list, x and y are coordinates, and w is the width.
    # Also note that the y-axis goes from top to bottom, not bottom to top like how it usually does.
    newBoard[3 + 8*3] = classes.Disc(True, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[4 + 8*3] = classes.Disc(False, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[3 + 8*4] = classes.Disc(False, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newBoard[4 + 8*4] = classes.Disc(True, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newGroup.add(newBoard[3 + 8*3])
    newGroup.add(newBoard[4 + 8*3])
    newGroup.add(newBoard[3 + 8*4])
    newGroup.add(newBoard[4 + 8*4])
    newGroup.draw(screen)

    return newBoard, newGroup

gameBoardList, gameBoardSpriteGroup = set_up_board(pygame.display.get_surface())
pygame.display.update()

while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True

    pygame.display.update()
    clock.tick(20)

pygame.quit()
