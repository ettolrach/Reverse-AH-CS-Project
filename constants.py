import pygame, os

def initialise():
	global RESOLUTION, SQUARE_SIZE, BOARD_SIZE, TOP_OFFSET, RIGHT_OFFSET, DIRECTIONS, BACKGROUND, BACKGROUND_COLOUR, DATABASE_PATH, TITLEFONT, LARGEFONT, MEDIUMFONT, SMALLFONT
	RESOLUTION = [640,720]
	pygame.display.set_mode(RESOLUTION)
	BACKGROUND = pygame.image.load(os.path.join("sprites", "gameBoard.png")).convert()
	BACKGROUND_COLOUR = pygame.Color(000,144,103)
	SQUARE_SIZE = 80
	BOARD_SIZE = 8
	TOP_OFFSET = 40
	RIGHT_OFFSET = 1
	DIRECTIONS = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1, 0), (-1,-1)]
	DATABASE_PATH = os.path.join("db", "database.py")
	TITLEFONT = pygame.font.SysFont("Georgia", 60)
	LARGEFONT = pygame.font.SysFont("TW Cen MT", 36)
	MEDIUMFONT = pygame.font.SysFont("TW Cen MT", 26)
	SMALLFONT = pygame.font.SysFont("TW Cen MT", 20)
