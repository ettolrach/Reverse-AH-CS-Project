import pygame
pygame.init()
import functions, constants, classes, database
from pygame.constants import MOUSEBUTTONUP

# Initialise top-level variables
windowTitle = "Reverse!"
stopGame = False
pygame.display.set_mode(constants.RESOLUTION)
pygame.display.set_caption(windowTitle)
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
newScene = ""

currentScene = classes.MainMenu()

# Set up database and create some sample data.
database.prepare_database()
database.drop_highscore_table()
database.create_highscore_table()
database.add_new_highscore("Alice", 35)
database.add_new_highscore("Bob", 39)
database.add_new_highscore("Cerys", 40)
database.add_new_highscore("Dean", 42)
database.add_new_highscore("Emily", 43)
database.add_new_highscore("Frederick", 48)
database.add_new_highscore("Garry", 49)
database.add_new_highscore("Hannah", 51)
database.add_new_highscore("Ian", 54)
database.add_new_highscore("Jebeddiah", 58)

# Main game loop.
while stopGame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stopGame = True
        elif event.type == MOUSEBUTTONUP:
            newScene = currentScene.click()
            if newScene == "mainmenu":
                currentScene = classes.MainMenu()
                windowTitle = "Main Menu - Reverse!"
                pygame.display.set_caption(windowTitle)
            if newScene == "namescreen":
                currentScene = classes.NameScreen()
                windowTitle = "Name Selection - Reverse!"
                pygame.display.set_caption(windowTitle)
            if newScene == "game":
                names = []
                # Add the contents of the textboxes to a list for later.
                for textbox in currentScene.textboxGroup:
                    names.append(textbox.text)
                currentScene = classes.Game(names)
                windowTitle = "Game - Reverse!"
                pygame.display.set_caption(windowTitle)
            if newScene == "highscores":
                currentScene = classes.HighScores()
                windowTitle = "High Scores - Reverse!"
                pygame.display.set_caption(windowTitle)
            if newScene == "quit":
                stopGame = True
        else:
            if windowTitle == "Name Selection - Reverse!" and event.type == pygame.KEYDOWN:
                currentScene.keyPress(event)

    currentScene.update()
    clock.tick(20)

pygame.quit()
