import pygame

class Disc(pygame.sprite.Sprite):
    def __init__(self, initialColour):
        pygame.sprite.Sprite.__init__(self)
        self.colour = initialColour
        self.image = pygame.Surface([79,79])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def change_coordinates(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY
    
    def change_image(self, newImg):
        self.image.blit(pygame.image.load(newImg), (0,0))

class Board:
    def __init__(self, boardSize):
        # As the board is a square, "boardSize" is the length of each side in unit squares.
        self.size = boardSize
        # Create a 2D list full of None.
        # Do note that instead of the standard (x, y) notation for coordinates, this will use [y][x] to refer to a coordinate, and the y-axis is going downwards!
        self.squares = [[None for i in range(boardSize)] for j in range(boardSize)]
        # Create the standard starting position.
        self.squares[4][4] = Disc("white")
        self.squares[4][5] = Disc("black")
        self.squares[5][4] = Disc("white")
        self.squares[5][5] = Disc("black")
