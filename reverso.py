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
gameOver = False

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
            if gameOver == True:
                stopGame = True
            else:
                # Get the x and y coordinates from the pixel value of the mouse click.
                x = int((pygame.mouse.get_pos()[0] - constants.RIGHT_OFFSET) / constants.SQUARE_SIZE)
                y = int((pygame.mouse.get_pos()[1] - constants.TOP_OFFSET) / constants.SQUARE_SIZE)
                totalFlip = []

                # Make a move.
                totalFlip = functions.make_move(boardList, x, y, whiteToPlay)
                # If the move was legal,
                if totalFlip != []:
                    # flip the discs at the coordinates in the list 'totalFlip'.
                    for index in totalFlip:
                        boardList, white_counter, black_counter = functions.change_colour_of_disc(boardList, index, white_counter, black_counter)

                    # and place the disc at the clicked coordinate and update appropriate variables.
                    boardList, boardSpriteGroup, white_counter, black_counter = functions.place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter)
                    # Log the move for debugging purposes.
                    xLetter = chr(97+x)
                    print(xLetter + str(y+1))

                    if white_counter + black_counter == 64:
                        if white_counter > black_counter:
                            functions.draw_everything(boardSpriteGroup, largeFont, True, white_counter, black_counter, " Wins!")
                            whoseMoveImage = largeFont.render("Click anywhere to quit.", True, "white").convert_alpha()
                            pygame.display.get_surface().blit(whoseMoveImage, (160 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
                        elif black_counter > white_counter:
                            functions.draw_everything(boardSpriteGroup, largeFont, False, white_counter, black_counter, " Wins!")
                            whoseMoveImage = largeFont.render("Click anywhere to quit.", True, "black").convert_alpha()
                            pygame.display.get_surface().blit(whoseMoveImage, (480 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
                        else:
                            whoseMoveImage = largeFont.render("It is a draw.", True, "black").convert_alpha()
                            pygame.display.get_surface().blit(whoseMoveImage, (480 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
                        
                            whoseMoveImage = largeFont.render("Click anywhere to quit.", True, "white").convert_alpha()
                            pygame.display.get_surface().blit(whoseMoveImage, (160 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
                        gameOver = True
                        break

                    whiteToPlay = not whiteToPlay
                    # Check if now there are legal moves and the board hasn't filled up.
                    if functions.are_legal_moves_available(boardList, x, y, whiteToPlay) != True:
                        whiteToPlay = not whiteToPlay
                        if functions.are_legal_moves_available(boardList, x, y, whiteToPlay) != True:
                            functions.draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter, " Wins!")
                            gameOver = True
                            break

                functions.draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter)

    pygame.display.update()
    clock.tick(20)

pygame.quit()
