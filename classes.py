import pygame, os, constants, functions

class Button(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height, bdrWidth, bgColour, bdrInactiveColour, bdrActiveColour, text, fontToUse, fontColour, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.borderWidth = bdrWidth
        self.backgroundColour = bgColour
        self.borderInactiveColour = bdrInactiveColour
        self.borderActiveColour = bdrActiveColour
        self.text = text
        self.font = fontToUse
        self.fontColour = fontColour
        self.rect.x = xPos
        self.rect.y = yPos
        self.rect.width = width
        self.rect.height = height
        self.active = False
        self.sceneName = name

    def draw(self):
        # Draw the border.
        bdrSurface = pygame.Surface((self.rect.width, self.rect.height))
        if (self.active == False):
            bdrSurface.fill(self.borderInactiveColour)
        else:
            bdrSurface.fill(self.borderActiveColour)
        pygame.display.get_surface().blit(bdrSurface, (self.rect.x, self.rect.y))

        # Draw the background.
        bgSurface = pygame.Surface((self.rect.width - 2 * self.borderWidth, self.rect.height - 2 * self.borderWidth))
        bgSurface.fill(self.backgroundColour)
        pygame.display.get_surface().blit(bgSurface, (self.rect.x + self.borderWidth, self.rect.y + self.borderWidth))

        # Render the text that's to be displayed.
        fontImage = self.font.render(self.text, True, self.fontColour).convert_alpha()
        # Draw this text.
        pygame.display.get_surface().blit(fontImage, (self.rect.x + (self.rect.width / 2 - fontImage.get_width() / 2), self.rect.y + (self.rect.height / 2 - fontImage.get_height() / 2)))

        # Draw the background colour of the button.
        #self.image.fill(self.backgroundColour)
        # Blit the text on top of the background colour.
        # The calculations are there to centre the text.
        #self.image.blit(fontImage, (270, 300))
        #self.image.blit(fontImage, ((self.rect.x + self.rect.width / 2) - fontImage.get_width() / 2, (self.rect.y + self.rect.height / 2) - fontImage.get_height() / 2))

    def collide(self, pos):
        if (pos[0] >= self.rect.x and pos[0] <= self.rect.x + self.rect.width) and (pos[1] >= self.rect.y and pos[1] <= self.rect.y + self.rect.height):
            return True
        else:
            return False

class Scene():
    def __init__(self, bgColour):
        # When the scene gets shown for the first time, the whole screen will be cleared.
        pygame.display.get_surface().fill(bgColour)
        self.update([pygame.Rect(0, 0, constants.RESOLUTION[0], constants.RESOLUTION[1])])
    
    def update(self, rects = [None]):
        pygame.display.update(rects)

class MainMenu(Scene):
    def __init__(self):
        # Create buttons in the buttonGroup.
        self.buttonGroup = [
            Button(constants.RESOLUTION[0] / 2 - 100, 300, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Start Game", constants.MEDIUMFONT, pygame.Color("white"), "game"),
            Button(constants.RESOLUTION[0] / 2 - 100, 375, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "View High Scores", constants.MEDIUMFONT, pygame.Color("white"), "highscores"),
            Button(constants.RESOLUTION[0] / 2 - 100, 450, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Quit", constants.MEDIUMFONT, pygame.Color("white"), "quit")
        ]

        super().__init__(constants.BACKGROUND_COLOUR)
    
    def update(self, changedAreas = []):
        # Check if any buttons is hovered on and draw each button.
        for button in self.buttonGroup:
            if button.collide(pygame.mouse.get_pos()):
                button.active = True
            else:
                button.active = False
            button.draw()
            changedAreas.append(button.rect)

        # Draw the name of the game and append the area where the text is to the list changedAreas.
        changedAreas.append(functions.draw_text_centred(constants.TITLEFONT, "Reverse!", pygame.Color("black"), constants.RESOLUTION[0] / 2, 100))
        super().update(changedAreas)
    
    def click(self):
        for button in self.buttonGroup:
            if button.active == True:
                return button.sceneName
        return ""

class Game(Scene):
    def __init__(self):
        self.whiteCounter = 0
        self.blackCounter = 0
        self.gameOver = False
        self.whiteToPlay = False
        self.boardList, self.boardSpriteGroup, self.whiteCounter, self.blackCounter, self.currentState = functions.set_up_board(self.whiteCounter, self.blackCounter, constants.LARGEFONT)
    
    def click(self):
        if self.gameOver == True:
            return "mainmenu"
        else:
            # Get the x and y coordinates from the pixel value of the mouse click.
            x = int((pygame.mouse.get_pos()[0] - constants.RIGHT_OFFSET) / constants.SQUARE_SIZE)
            y = int((pygame.mouse.get_pos()[1] - constants.TOP_OFFSET) / constants.SQUARE_SIZE)
            
            self.boardList, self.boardSpriteGroup, self.whiteToPlay, self.whiteCounter, self.blackCounter, self.gameOver = functions.make_move(self.boardList, self.boardSpriteGroup, constants.LARGEFONT, x, y, self.whiteToPlay, self.whiteCounter, self.blackCounter)

class HighScores(Scene):
    def __init__(self):
        self.buttonGroup = [
            Button(constants.RESOLUTION[0]//3 - 175, 650, 250, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Back to Main Menu", constants.MEDIUMFONT, pygame.Color("white"), "mainmenu")
        ]
        super().__init__(constants.BACKGROUND_COLOUR)
    
    def update(self, changedAreas = []):
        # Check if any buttons is hovered on and draw each button.
        for button in self.buttonGroup:
            if button.collide(pygame.mouse.get_pos()):
                button.active = True
            else:
                button.active = False
            button.draw()
            changedAreas.append(button.rect)
        
        super().update(changedAreas)
    
    def click(self):
        for button in self.buttonGroup:
            if button.active == True:
                return button.sceneName
        return ""

class Disc(pygame.sprite.Sprite):
    def __init__(self, isWhiteInitially, xPos, yPos):
        pygame.sprite.Sprite.__init__(self)
        self.isWhite = isWhiteInitially
        self.image = pygame.Surface([78,78])
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos

        if isWhiteInitially == True:
            self.image = pygame.image.load(os.path.join("sprites", "whiteDisc.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join("sprites", "blackDisc.png")).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (78,78))
    
    def change_colour(self):
        if self.isWhite == True:
            self.image = pygame.image.load(os.path.join("sprites", "blackDisc.png")).convert_alpha()
            self.isWhite = False
        else:
            self.image = pygame.image.load(os.path.join("sprites", "whiteDisc.png")).convert_alpha()
            self.isWhite = True
        self.image = pygame.transform.smoothscale(self.image, (78,78))
