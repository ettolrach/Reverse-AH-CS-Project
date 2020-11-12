import pygame, classes, constants

def set_up_board(screen, white_counter, black_counter):
    # Create a new sprite group to work with the graphics of PyGame easier.
    newGroup = pygame.sprite.Group()
    # Create a 1D list of a 2D grid.
    newBoard = [None for i in range(constants.BOARD_SIZE**2)]
    # Use i = x + wy where i is the desired index in the 1D list, x and y are coordinates, and w is the width.
    # Also note that the y-axis goes from TOP TO BOTTOM, not bottom to top like how it usually does.

    # Set up the starting position.
    newBoard[3 + constants.BOARD_SIZE*3] = classes.Disc(True, constants.RIGHT_OFFSET + 3 * constants.SQUARE_SIZE, constants.TOP_OFFSET + 3 * constants.SQUARE_SIZE)
    newBoard[4 + constants.BOARD_SIZE*3] = classes.Disc(False, constants.RIGHT_OFFSET + 4 * constants.SQUARE_SIZE, constants.TOP_OFFSET + 3 * constants.SQUARE_SIZE)
    newBoard[3 + constants.BOARD_SIZE*4] = classes.Disc(False, constants.RIGHT_OFFSET + 3 * constants.SQUARE_SIZE, constants.TOP_OFFSET + 4 * constants.SQUARE_SIZE)
    newBoard[4 + constants.BOARD_SIZE*4] = classes.Disc(True, constants.RIGHT_OFFSET + 4 * constants.SQUARE_SIZE, constants.TOP_OFFSET + 4 * constants.SQUARE_SIZE)
    newGroup.add(newBoard[3 + constants.BOARD_SIZE*3], newBoard[4 + constants.BOARD_SIZE*3], newBoard[3 + constants.BOARD_SIZE*4], newBoard[4 + constants.BOARD_SIZE*4])
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
    if boardList[x + constants.BOARD_SIZE*y] != None:
        return listToFlip

    while True:
        # Apply the vector specified.
        x += changeX
        y += changeY

        # Note that it's okay to use multiple 'if's here since all except the last return values.
        # If x and y are out of bounds, then no discs should be flipped.
        if y < 0 or x < 0 or y > 7 or x > 7:
            return []
        # If the run ends in an empty square, then no discs should be flipped.
        if boardList[x + constants.BOARD_SIZE*y] == None:
            return []
        # If another of the same colour is found, then there could be discs to flip if 'listToFlip' has been modified and the run has ended.
        if boardList[x + constants.BOARD_SIZE*(y)].isWhite is whiteToPlay:
            break
        # If all of those checks fail, then the disc should be flipped and is added to the list.
        listToFlip.append(x + constants.BOARD_SIZE*y)

    return listToFlip

def make_move(boardList, x, y, whiteToPlay):
    # Keep track of all the discs that should be flipped.
    totalFlip = []
    # Check for discs to flip in all of the constants.DIRECTIONS using tuplets defined as a constant at the global level.
    # These are referred to as vectors.
    for direction in constants.DIRECTIONS:
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
    for y in range(constants.BOARD_SIZE):
        for x in range(constants.BOARD_SIZE):
            # Use the make_move function to check if there is a move available.
            # If at any point there is a move available, then there are indeed legal moves available.
            if make_move(boardList, x, y, whiteToPlay) != []:
                return True
    return False

def place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, white_counter, black_counter):
    # Update the list of discs and sprite group.
    boardList[x + constants.BOARD_SIZE*y] = classes.Disc(whiteToPlay, constants.RIGHT_OFFSET + x * constants.SQUARE_SIZE, constants.TOP_OFFSET + y * constants.SQUARE_SIZE)
    boardSpriteGroup.add(boardList[x + constants.BOARD_SIZE*y])

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
    pygame.display.get_surface().blit(constants.BACKGROUND, (0,0))
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
