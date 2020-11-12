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
black_counter = 0
white_counter = 0

def set_up_board(screen, white_counter, black_counter):
    # Create a new sprite group to work with the graphics of PyGame easier.
    newGroup = pygame.sprite.Group()
    # Create a 1D list of a 2D grid.
    newBoard = [None for i in range(BOARD_SIZE**2)]
    # Use i = x + wy where i is the desired index in the 1D list, x and y are coordinates, and w is the width.
    # Also note that the y-axis goes from TOP TO BOTTOM, not bottom to top like how it usually does.

    # Set up the starting position.
    newBoard[3 + BOARD_SIZE*3] = classes.Disc(True, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[4 + BOARD_SIZE*3] = classes.Disc(False, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 3 * SQUARE_SIZE)
    newBoard[3 + BOARD_SIZE*4] = classes.Disc(False, RIGHT_OFFSET + 3 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newBoard[4 + BOARD_SIZE*4] = classes.Disc(True, RIGHT_OFFSET + 4 * SQUARE_SIZE, TOP_OFFSET + 4 * SQUARE_SIZE)
    newGroup.add(newBoard[3 + BOARD_SIZE*3], newBoard[4 + BOARD_SIZE*3], newBoard[3 + BOARD_SIZE*4], newBoard[4 + BOARD_SIZE*4])
    # Set up the counters to match.
    black_counter = 2
    white_counter = 2

    newGroup.draw(screen)

    return newBoard, newGroup, white_counter, black_counter

def change_colour_of_disc(boardList, index, white_counter, black_counter):
    # Update the counters.
    if boardList[index].isWhite == True:
        black_counter += 1
        white_counter -= 1
    else:
        black_counter -= 1
        white_counter += 1
    # Change the colour and return the modified list of discs.    
    boardList[index].change_colour()

    return boardList, white_counter, black_counter

def get_discs_to_flip(boardList, x, y, changeX, changeY, whiteToPlay):
    # This list will keep track of all the indicies of discs that should be flipped.
    listToFlip = []
    # Check whether the sqaure that was clicked is empty. If it isn't, then it's an illegal move.
    if (boardList[x + BOARD_SIZE*y] != None):
        return listToFlip

    while True:
        # Apply the vector specified.
        x += changeX
        y += changeY

        # Note that it's okay to use multiple 'if's here since all except the last return values.
        # If x and y are out of bounds, then no discs should be flipped.
        if (y < 0 or x < 0 or y > 7 or x > 7):
            return []
        # If the run ends in an empty square, then no discs should be flipped.
        if boardList[x + BOARD_SIZE*y] == None:
            return []
        # If another of the same colour is found, then there could be discs to flip if 'listToFlip' has been modified and the run has ended.
        if boardList[x + BOARD_SIZE*(y)].isWhite is whiteToPlay:
            break
        # If all of those checks fail, then the disc should be flipped and is added to the list.
        listToFlip.append(x + BOARD_SIZE*y)

    return listToFlip

def make_move(boardList, x, y, whiteToPlay):
    # Keep track of all the discs that should be flipped.
    totalFlip = []
    # Check for discs to flip in all of the directions using tuplets defined as a constant at the global level.
    # These are referred to as vectors.
    for direction in DIRECTIONS:
        # Run an algorithm which finds discs to flip in a specified direction.
        toFlip = get_discs_to_flip(boardList, x, y, direction[0], direction[1], whiteToPlay)
        # If there are no discs to be flipped, check the next direction.
        if (toFlip == []):
            continue
        # Otherwise, add the list onto the 'totalFlip' list.
        totalFlip.extend(toFlip)

    return totalFlip

def are_legal_moves_available(boardList, x, y, whiteToPlay):
    # Run through all of the indicies.
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            # Use the make_move function to check if there is a move available.
            # If at any point there is a move available, then there are indeed legal moves available.
            if make_move(boardList, x, y, whiteToPlay) != []:
                return True
    return False

def place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter):
    # Update the list of discs and sprite group.
    boardList[x + BOARD_SIZE*y] = classes.Disc(whiteToPlay, RIGHT_OFFSET + x * SQUARE_SIZE, TOP_OFFSET + y * SQUARE_SIZE)
    boardSpriteGroup.add(boardList[x + BOARD_SIZE*y])

    # Update the counter.
    if whiteToPlay == True:
        white_counter += 1
    else:
        black_counter += 1

    # Change whose turn it is.
    whiteToPlay = not whiteToPlay

    return boardList, boardSpriteGroup, whiteToPlay, white_counter, black_counter

def draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter):
    # Draw the discs.
    pygame.display.get_surface().blit(background, (0,0))
    boardSpriteGroup.draw(pygame.display.get_surface())

    # Draw the "[COLOUR] To Play" text.
    if whiteToPlay == True:
        whoseMoveImage = largeFont.render("White To Play", True, "black").convert_alpha()
        pygame.display.get_surface().blit(whoseMoveImage, (480 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))
    else:
        whoseMoveImage = largeFont.render("Black To Play", True, "white").convert_alpha()
        pygame.display.get_surface().blit(whoseMoveImage, (160 - whoseMoveImage.get_width() / 2, 20 - whoseMoveImage.get_height() / 2))

    # Draw the disc counters.
    whiteCounter = largeFont.render(str(white_counter), True, "black").convert_alpha()
    blackCounter = largeFont.render(str(black_counter), True, "white").convert_alpha()
    pygame.display.get_surface().blit(whiteCounter, (480 - whiteCounter.get_width() / 2, 700 - whiteCounter.get_height() / 2))
    pygame.display.get_surface().blit(blackCounter, (160 - blackCounter.get_width() / 2, 700 - blackCounter.get_height() / 2))

# Initialise the board.
boardList, boardSpriteGroup, white_counter, black_counter = set_up_board(pygame.display.get_surface(), white_counter, black_counter)
draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter)
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

            # Check if there are moves available.
            if are_legal_moves_available(boardList, x, y, whiteToPlay) == True:
                # If they are, make a move.
                totalFlip = make_move(boardList, x, y, whiteToPlay)
                # If the move was legal,
                if totalFlip != []:
                    # then flip the discs at the coordinates in the list 'totalFlip'.
                    for index in totalFlip:
                        boardList, white_counter, black_counter = change_colour_of_disc(boardList, index, white_counter, black_counter)

                    # and place the disc at the clicked coordinate and update appropriate variables.
                    boardList, boardSpriteGroup, whiteToPlay, white_counter, black_counter = place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter)
                    # Log the move for debugging purposes.
                    xLetter = chr(97+x)
                    print(xLetter + str(y+1))
            else:
                boardList, boardSpriteGroup, whiteToPlay, white_counter, black_counter = place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter)
                # Log the move for debugging purposes.
                xLetter = chr(97+x)
                print(xLetter + str(y+1))
            
            draw_everything(boardSpriteGroup, largeFont, whiteToPlay, white_counter, black_counter)

    pygame.display.update()
    clock.tick(20)

pygame.quit()
