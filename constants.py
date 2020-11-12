import pygame, os

def initialise():
	global RESOLUTION, SQUARE_SIZE, BOARD_SIZE, TOP_OFFSET, RIGHT_OFFSET, DIRECTIONS, BACKGROUND
	RESOLUTION = [640,720]
	pygame.display.set_mode(RESOLUTION)
	BACKGROUND = pygame.image.load(os.path.join("sprites", "gameBoard.png")).convert()
	SQUARE_SIZE = 80
	BOARD_SIZE = 8
	TOP_OFFSET = 40
	RIGHT_OFFSET = 1
	DIRECTIONS = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0), (-1,-1)]
