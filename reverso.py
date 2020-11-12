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
largeFont = pygame.font.SysFont("TW Cen MT", 36)
smallFont = pygame.font.SysFont("TW Cen MT", 20)
black_counter = 0
white_counter = 0

# Initialise the board.
boardList, boardSpriteGroup, white_counter, black_counter = functions.set_up_board(pygame.display.get_surface(), white_counter, black_counter)
functions.draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter)
pygame.display.update()

# Main game loop.
while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        if event.type == MOUSEBUTTONDOWN:
            # Get the x and y coordinates from the pixel value of the mouse click.
            x = int((pygame.mouse.get_pos()[0] - constants.RIGHT_OFFSET) / constants.SQUARE_SIZE)
            y = int((pygame.mouse.get_pos()[1] - constants.TOP_OFFSET) / constants.SQUARE_SIZE)
            totalFlip = []

            # Check if there are moves available.
            if functions.are_legal_moves_available(boardList, x, y, whiteToPlay) == True:
                # If they are, make a move.
                totalFlip = functions.make_move(boardList, x, y, whiteToPlay)
                # If the move was legal,
                if totalFlip != []:
                    # then flip the discs at the coordinates in the list 'totalFlip'.
                    for index in totalFlip:
                        boardList, white_counter, black_counter = functions.change_colour_of_disc(boardList, index, white_counter, black_counter)

                    # and place the disc at the clicked coordinate and update appropriate variables.
                    boardList, boardSpriteGroup, whiteToPlay, white_counter, black_counter = functions.place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter)
                    # Log the move for debugging purposes.
                    xLetter = chr(97+x)
                    print(xLetter + str(y+1))
            else:
                boardList, boardSpriteGroup, whiteToPlay, white_counter, black_counter = functions.place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter)
                # Log the move for debugging purposes.
                xLetter = chr(97+x)
                print(xLetter + str(y+1))
            
            functions.draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter)

    pygame.display.update()
    clock.tick(20)

pygame.quit()
