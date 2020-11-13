import pygame, classes, constants

def set_up_board(screen, whiteCounter, blackCounter):
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
    blackCounter = 2
    whiteCounter = 2

    newGroup.draw(screen)

    return newBoard, newGroup, whiteCounter, blackCounter

def change_colour_of_disc(boardList, index, whiteCounter, blackCounter):
    # Update the counters.
    if boardList[index].isWhite == True:
        blackCounter += 1
        whiteCounter -= 1
    else:
        blackCounter -= 1
        whiteCounter += 1
    # Change the colour and return the modified list of discs.    
    boardList[index].change_colour()

    return boardList, whiteCounter, blackCounter

def get_discs_to_flip_in_one_direction(boardList, x, y, changeX, changeY, whiteToPlay):
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

def get_all_discs_to_flip(boardList, x, y, whiteToPlay):
    # Keep track of all the discs that should be flipped.
    totalFlip = []
    # Check for discs to flip in all of the constants.DIRECTIONS using tuplets defined as a constant at the global level.
    # These are referred to as vectors.
    for direction in constants.DIRECTIONS:
        # Run an algorithm which finds discs to flip in a specified direction.
        toFlip = get_discs_to_flip_in_one_direction(boardList, x, y, direction[0], direction[1], whiteToPlay)
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
            if get_all_discs_to_flip(boardList, x, y, whiteToPlay) != []:
                return True
    return False

def place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter):
    # Update the list of discs and sprite group.
    boardList[x + constants.BOARD_SIZE*y] = classes.Disc(whiteToPlay, constants.RIGHT_OFFSET + x * constants.SQUARE_SIZE, constants.TOP_OFFSET + y * constants.SQUARE_SIZE)
    boardSpriteGroup.add(boardList[x + constants.BOARD_SIZE*y])

    # Update the counter.
    if whiteToPlay == True:
        whiteCounter += 1
    else:
        blackCounter += 1

    return boardList, boardSpriteGroup, whiteCounter, blackCounter

def draw_everything(boardSpriteGroup, fontToUse, whiteToPlay, whiteCounter, blackCounter, colourWins = False, draw = False):
    # Draw the discs.
    pygame.display.get_surface().blit(constants.BACKGROUND, (0,0))
    boardSpriteGroup.draw(pygame.display.get_surface())

    # Draw the appropriate text.
    if colourWins == True:
        if whiteToPlay == True:
            draw_text_centred(fontToUse, "White Wins!", "black", 480, 20)
            draw_text_centred(fontToUse, "Click anywhere to quit.", "white", 160, 20)
        else:
            draw_text_centred(fontToUse, "Black Wins!", "white", 160, 20)
            draw_text_centred(fontToUse, "Click anywhere to quit.", "black", 480, 20)
    elif draw == True:
        draw_text_centred(fontToUse, "It is a draw.", "white", 160, 20)
        draw_text_centred(fontToUse, "Click anywhere to quit.", "black", 480, 20)
    else:
        if whiteToPlay == True:
            draw_text_centred(fontToUse, "White To Play", "black", 480, 20)
        else:
            draw_text_centred(fontToUse, "Black To Play", "white", 160, 20)

    # Draw the disc counters.
    draw_text_centred(fontToUse, str(blackCounter), "white", 160, 700)
    draw_text_centred(fontToUse, str(whiteCounter), "black", 480, 700)

def draw_text_centred(fontToUse, text, colour, xCentre = 0, yCentre = 0):
    fontImage = fontToUse.render(text, True, colour).convert_alpha()
    pygame.display.get_surface().blit(fontImage, (xCentre - fontImage.get_width() / 2, yCentre - fontImage.get_height() / 2))

def make_move(boardList, boardSpriteGroup, fontToUse, x, y, whiteToPlay, whiteCounter, blackCounter):
    totalFlip = []
    gameOver = False

    # Make a move.
    totalFlip = get_all_discs_to_flip(boardList, x, y, whiteToPlay)
    # If the move was legal,
    if totalFlip != []:
        # flip the discs at the coordinates in the list 'totalFlip'.
        for index in totalFlip:
            boardList, whiteCounter, blackCounter = change_colour_of_disc(boardList, index, whiteCounter, blackCounter)

        # and place the disc at the clicked coordinate and update appropriate variables.
        boardList, boardSpriteGroup, whiteCounter, blackCounter = place_disc(boardList, x, y, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter)
        # Log the move for debugging purposes.
        xLetter = chr(97+x)
        print(xLetter + str(y+1), end = " ")

        if whiteCounter + blackCounter == 64:
            if whiteCounter > blackCounter:
                draw_everything(boardSpriteGroup, fontToUse, True, whiteCounter, blackCounter, True)
            elif blackCounter > whiteCounter:
                draw_everything(boardSpriteGroup, fontToUse, False, whiteCounter, blackCounter, True)
            else:
                draw_everything(boardSpriteGroup, fontToUse, whiteToPlay, whiteCounter, blackCounter, False, True)
            gameOver = True
            return boardList, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter, gameOver

        whiteToPlay = not whiteToPlay
        # Check if now there are legal moves and the board hasn't filled up.
        if are_legal_moves_available(boardList, x, y, whiteToPlay) != True:
            whiteToPlay = not whiteToPlay
            if are_legal_moves_available(boardList, x, y, whiteToPlay) != True:
                draw_everything(boardSpriteGroup, fontToUse, whiteToPlay, whiteCounter, blackCounter, True)
                gameOver = True
                return boardList, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter, gameOver

    draw_everything(boardSpriteGroup, fontToUse, whiteToPlay, whiteCounter, blackCounter)
    return boardList, boardSpriteGroup, whiteToPlay, whiteCounter, blackCounter, gameOver
