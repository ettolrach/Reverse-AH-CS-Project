import pygame, classes, os
from pygame.constants import MOUSEBUTTONDOWN
pygame.init()

# Game variables
windowTitle = "Reverso"
stopGame = False
backgroundColour = ( 96,191, 77)
black = (  0,  0,  0)
whiteToPlay = True
RESOLUTION = [640,720]
SQUARE_SIZE = 80
BOARD_SIZE = 8
TOP_OFFSET = 40
RIGHT_OFFSET = 1
DIRECTIONS = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0), (-1,-1)]

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
    newBoard[3 + BOARD_SIZE*3] = classes.Disc(True, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[4 + BOARD_SIZE*3] = classes.Disc(False, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[3 + BOARD_SIZE*4] = classes.Disc(False, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newBoard[4 + BOARD_SIZE*4] = classes.Disc(True, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newGroup.add(newBoard[3 + BOARD_SIZE*3], newBoard[4 + BOARD_SIZE*3], newBoard[3 + BOARD_SIZE*4], newBoard[4 + BOARD_SIZE*4])
    newGroup.draw(screen)

    return newBoard, newGroup

def get_discs_to_flip(boardList, x, y, changeX, changeY, whiteToPlay):
    listToFlip = []
    # Check whether the sqaure that was clicked is empty. If it isn't, then it's an illegal move.
    if (boardList[x + BOARD_SIZE*y] != None):
        return listToFlip
    while True:
        x += changeX
        y += changeY

        if y <= 0 or x <= 0 or y >= 8 or x >= 8:
            break

        if (boardList[x + BOARD_SIZE*y] == None or boardList[x + BOARD_SIZE*(y)].isWhite is whiteToPlay):
            if boardList[x + BOARD_SIZE*y] == None:
                listToFlip.clear()
            break
        listToFlip.append(x + BOARD_SIZE*y)

    return listToFlip

boardList, boardSpriteGroup = set_up_board(pygame.display.get_surface())
pygame.display.update()

while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        if event.type == MOUSEBUTTONDOWN:
            x = int((pygame.mouse.get_pos()[0] - RIGHT_OFFSET) / SQUARE_SIZE)
            y = int((pygame.mouse.get_pos()[1] - TOP_OFFSET) / SQUARE_SIZE)

            totalFlip = []
            for direction in DIRECTIONS:
                toFlip = get_discs_to_flip(boardList, x, y, direction[0], direction[1], whiteToPlay)
                if (toFlip == []):
                    continue
                totalFlip.extend(toFlip)
            
            if len(totalFlip) > 0:
                for index in totalFlip:
                    boardList[index].change_colour()
                boardList[x + BOARD_SIZE*y] = classes.Disc(whiteToPlay, RIGHT_OFFSET + x * SQUARE_SIZE, TOP_OFFSET + y * SQUARE_SIZE)
                boardSpriteGroup.add(boardList[x + BOARD_SIZE*y])
                whiteToPlay = not whiteToPlay
                xLetter = chr(97+x)
                print(xLetter + str(y))
            boardSpriteGroup.draw(pygame.display.get_surface())

    pygame.display.update()
    clock.tick(20)

pygame.quit()
