import pygame
pygame.init()
import functions, constants, classes
from pygame.constants import MOUSEBUTTONUP

# Initialise top-level variables
windowTitle = "Reverse!"
stopGame = False
pygame.display.set_mode(constants.RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

currentScene = classes.MainMenu()

# Main game loop.
while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        if event.type == MOUSEBUTTONUP:
            newScene = currentScene.click()
            if newScene == "mainmenu":
                currentScene = classes.MainMenu()
            if newScene == "game":
                currentScene = classes.Game()
            if newScene == "highscores":
                currentScene = classes.HighScores()
            if newScene == "quit":
                stopGame = True

    currentScene.update()
    clock.tick(20)

pygame.quit()
