import pygame, classes, os
from pygame.constants import MOUSEBUTTONDOWN
pygame.init()

# Game variables
windowTitle = "Reverse!"
stopGame = False
backgroundColour = ( 96,191, 77)
RESOLUTION = [640,720]
SQUARE_SIZE = 80
BOARD_SIZE = 8
TOP_OFFSET = 40
RIGHT_OFFSET = 1
DIRECTIONS = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0), (-1,-1)]

whiteToPlay = False
pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
background = pygame.image.load(os.path.join("sprites", "gameBoard.png")).convert()
largeFont = pygame.font.SysFont("TW Cen MT", 36)
smallFont = pygame.font.SysFont("TW Cen MT", 20)

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

        if (y < 0 or x < 0 or y > 7 or x > 7):
            return []
        if boardList[x + BOARD_SIZE*y] == None:
            return []
        elif boardList[x + BOARD_SIZE*(y)].isWhite is whiteToPlay:
            break
        listToFlip.append(x + BOARD_SIZE*y)
    return listToFlip

def make_move(boardList, x, y, whiteToPlay):
    totalFlip = []
    for direction in DIRECTIONS:
        toFlip = get_discs_to_flip(boardList, x, y, direction[0], direction[1], whiteToPlay)
        if (toFlip == []):
            continue
        totalFlip.extend(toFlip)

    return totalFlip

def are_legal_moves_available(boardList, x, y, whiteToPlay):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if make_move(boardList, x, y, whiteToPlay) != []:
                return True

def place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay):
    boardList[x + BOARD_SIZE*y] = classes.Disc(whiteToPlay, RIGHT_OFFSET + x * SQUARE_SIZE, TOP_OFFSET + y * SQUARE_SIZE)
    boardSpriteGroup.add(boardList[x + BOARD_SIZE*y])
    whiteToPlay = not whiteToPlay

    return boardList, boardSpriteGroup, whiteToPlay

def draw_everything(boardSpriteGroup, largeFont, whiteToPlay):
    pygame.display.get_surface().blit(background, (0,0))
    boardSpriteGroup.draw(pygame.display.get_surface())
    if whiteToPlay == True:
        whoseMoveImage = largeFont.render("White To Play", True, "black").convert_alpha()
        pygame.display.get_surface().blit(whoseMoveImage, (480 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
    else:
        whoseMoveImage = largeFont.render("Black To Play", True, "white").convert_alpha()
        pygame.display.get_surface().blit(whoseMoveImage, (160 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))

boardList, boardSpriteGroup = set_up_board(pygame.display.get_surface())
draw_everything(boardSpriteGroup, largeFont, whiteToPlay)
pygame.display.update()

# Main game loop.
while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        if event.type == MOUSEBUTTONDOWN:
            # Get the x and y coordinates from the pixel value of the mouse click.
            x = int((pygame.mouse.get_pos()[0] - RIGHT_OFFSET) / SQUARE_SIZE)
            y = int((pygame.mouse.get_pos()[1] - TOP_OFFSET) / SQUARE_SIZE)
            totalFlip = []

            if are_legal_moves_available(boardList, x, y, whiteToPlay) == True:
                totalFlip = make_move(boardList, x, y, whiteToPlay)
                if totalFlip != []:
                    # then flip the discs at the coordinates in the list 'totalFlip'.
                    for index in totalFlip:
                        boardList[index].change_colour()

                    # Place the disc at the clicked coordinate and update appropriate variables.
                    boardList, boardSpriteGroup, whiteToPlay = place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay)
                    # Log the move for debugging purposes.
                    xLetter = chr(97+x)
                    print(xLetter + str(y+1))
            else:
                boardList, boardSpriteGroup, whiteToPlay = place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay)
                # Log the move for debugging purposes.
                xLetter = chr(97+x)
                print(xLetter + str(y+1))
            
            draw_everything(boardSpriteGroup, largeFont, whiteToPlay)

    pygame.display.update()
    clock.tick(20)

pygame.quit()
