import pygame, functions, constants
from pygame.constants import MOUSEBUTTONDOWN
pygame.init()

# Initialise global constants.
constants.initialise()

# Initialise top-level variables
windowTitle = "Reverse!"
stopGame = False
whiteToPlay = False
pygame.display.set_mode(constants.RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
titleFont = pygame.font.SysFont("Georgia", 60)
largeFont = pygame.font.SysFont("TW Cen MT", 36)
smallFont = pygame.font.SysFont("TW Cen MT", 20)
blackCounter = 0
whiteCounter = 0
gameOver = False
currentState = "mainMenu"

# Initialise the board.
boardList, boardSpriteGroup, whiteCounter, blackCounter, currentState = functions.set_up_board(pygame.display.get_surface(), whiteCounter, blackCounter, largeFont)

# To run certain moves for debug purposes, uncomment the following code and replace the example list.
"""
moves = ["e6", "f6", "f5", "f4", "f3", "d3", "c3", "c4", "c5", "d6", "e3", "g2", "f7", "c6", "g4", "d2", "b6", "b7", "c7", "e7", "g7", "g6", "g5", "h4", "h3", "h2", "h1", "f2", "g3", "e2", "c2", "b2", "b3", "b4", "b5", "d7", "b8", "c8", "d8", "f8", "g8", "e8", "h6", "h5", "g1", "f1", "e1", "d1", "c1", "b1", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8"]

for move in moves:
    # Get the x and y coordinates from the pixel value of the mouse click.
    x = int(ord(move[0]) - 97)
    y = int(move[1])-1
    
    boardList, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter = functions.make_move(boardList, boardSpriteGroup, largeFont, x, y, whiteToPlay, whiteCounter, blackCounter)
"""

# Main game loop.
while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        if event.type == MOUSEBUTTONDOWN:
            if gameOver == True:
                stopGame = True
            else:
                # Get the x and y coordinates from the pixel value of the mouse click.
                x = int((pygame.mouse.get_pos()[0] - constants.RIGHT_OFFSET) / constants.SQUARE_SIZE)
                y = int((pygame.mouse.get_pos()[1] - constants.TOP_OFFSET) / constants.SQUARE_SIZE)
                
                boardList, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter, gameOver = functions.make_move(boardList, boardSpriteGroup, largeFont, x, y, whiteToPlay, whiteCounter, blackCounter)

    pygame.display.update()
    clock.tick(20)

pygame.quit()
