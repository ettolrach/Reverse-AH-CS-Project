import pygame, os, constants, functions, database

from pygame.key import name

class Button(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height, bdrWidth, bgColour, bdrInactiveColour, bdrActiveColour, text, fontToUse, fontColour, name = ""):
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

    def collide(self, pos):
        if (pos[0] >= self.rect.x and pos[0] <= self.rect.x + self.rect.width) and (pos[1] >= self.rect.y and pos[1] <= self.rect.y + self.rect.height):
            return True
        else:
            return False

class ButtonScene():
    def __init__(self, buttonGroup, bgColour):
        self.buttonGroup = buttonGroup
        # When the scene gets shown for the first time, the whole screen will be cleared.
        pygame.display.get_surface().fill(bgColour)
        self.update([pygame.Rect(0, 0, constants.RESOLUTION[0], constants.RESOLUTION[1])])
    
    def update(self, changedRects = [None]):
        # Check if any buttons is hovered on and draw each button.
        for button in self.buttonGroup:
            if button.collide(pygame.mouse.get_pos()):
                button.active = True
            else:
                button.active = False
            button.draw()
            changedRects.append(button.rect)

        pygame.display.update(changedRects)
    
    def click(self):
        for button in self.buttonGroup:
            if button.active == True:
                return button.sceneName
        return ""

class MainMenu(ButtonScene):
    def __init__(self):
        # Create buttons in the buttonGroup.
        buttonGroup = [
            Button(constants.RESOLUTION[0] / 2 - 100, 300, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Start Game", constants.MEDIUMFONT, pygame.Color("white"), "namescreen"),
            Button(constants.RESOLUTION[0] / 2 - 100, 375, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "View High Scores", constants.MEDIUMFONT, pygame.Color("white"), "highscores"),
            Button(constants.RESOLUTION[0] / 2 - 100, 450, 200, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Quit", constants.MEDIUMFONT, pygame.Color("white"), "quit")
        ]

        super().__init__(buttonGroup, constants.BACKGROUND_COLOUR)

        # Draw the name of the game.
        pygame.display.update(functions.draw_text_centred(constants.TITLEFONT, "Reverse!", pygame.Color("black"), constants.RESOLUTION[0] / 2, 100))

    def update(self, changedAreas = []):
        super().update(changedAreas)
    
    def click(self):
        return super().click()

class Game():
    def __init__(self, names):
        self.whiteCounter = 0
        self.blackCounter = 0
        self.gameOver = False
        self.whiteToPlay = False
        self.boardList, self.boardSpriteGroup, self.whiteCounter, self.blackCounter, self.currentState = functions.set_up_board(self.whiteCounter, self.blackCounter, constants.LARGEFONT)
        self.players = names
    
    def update(self):
        pygame.display.update()
    
    def click(self):
        if self.gameOver == True:
            if self.blackCounter > self.whiteCounter:
                database.add_new_highscore(self.players[0], self.blackCounter)
            elif self.whiteCounter > self.blackCounter:
                database.add_new_highscore(self.players[1], self.whiteCounter)
            return "mainmenu"
        else:
            # Get the x and y coordinates from the pixel value of the mouse click.
            x = int((pygame.mouse.get_pos()[0] - constants.RIGHT_OFFSET) / constants.SQUARE_SIZE)
            y = int((pygame.mouse.get_pos()[1] - constants.TOP_OFFSET) / constants.SQUARE_SIZE)

            # Make sure that the coordinates aren't out of range.
            if x < 8 and y < 8:
                self.boardList, self.boardSpriteGroup, self.whiteToPlay, self.whiteCounter, self.blackCounter, self.gameOver = functions.make_move(self.boardList, self.boardSpriteGroup, constants.LARGEFONT, x, y, self.whiteToPlay, self.whiteCounter, self.blackCounter)

class HighScores(ButtonScene):
    def __init__(self):
        buttonGroup = [
            Button(constants.RESOLUTION[0]//3 - 175, 650, 250, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Back to Main Menu", constants.MEDIUMFONT, pygame.Color("white"), "mainmenu")
        ]

        super().__init__(buttonGroup, constants.BACKGROUND_COLOUR)

        # Draw the title of the scene.
        pygame.display.update(functions.draw_text_centred(constants.LARGEFONT, "Top 10 High Scores", pygame.Color("black"), constants.RESOLUTION[0] / 2, 75))

        scores = database.get_highscores()
        scores = functions.insertion_sort(scores)
        # Get the first 10 scores from the sorted list, these should be the biggest ones.
        scores = scores[:10]
        for i in range(len(scores)):
            functions.draw_text_centred(constants.LARGEFONT, str(i+1) + ". ", pygame.Color("black"), 50, 150 + 40 * i)
            functions.draw_text_centred(constants.LARGEFONT, scores[i].name, pygame.Color("black"), constants.RESOLUTION[0]/2, 150 + 40 * i)            
            functions.draw_text_centred(constants.LARGEFONT, str(scores[i].discs), pygame.Color("black"), constants.RESOLUTION[0] - 50, 150 + 40 * i)
    
    def update(self, changedAreas = []):
        super().update(changedAreas)
    
    def click(self):
        return super().click()

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

class ScoreRecord:
    def __init__(self, name, discs):
        self.name = name
        self.discs = discs

class NameScreen(ButtonScene):
    def __init__(self):
        changedAreas = []
        self.buttonGroup = [
            Button(constants.RESOLUTION[0] - 115, constants.RESOLUTION[1]/2 + 80, 90, 40, 3, pygame.Color("black"), pygame.Color(100, 100, 100, 255), pygame.Color("white"), "Play", constants.MEDIUMFONT, pygame.Color("white"), "game")
        ]

        # Create the textboxes.
        self.textboxGroup = [
            TextBox(50, constants.RESOLUTION[1] / 2 - 20, 450, 40, 3, pygame.Color("white"), pygame.Color(100, 100, 100, 255), pygame.Color("black"), constants.MEDIUMFONT, pygame.Color("black")),
            TextBox(50, constants.RESOLUTION[1] / 2 + 80, 450, 40, 3, pygame.Color("white"), pygame.Color(100, 100, 100, 255), pygame.Color("black"), constants.MEDIUMFONT, pygame.Color("black"))
        ]
        # Add the textboxes to the changed areas to be drawn.
        changedAreas += [
            pygame.Rect(50, constants.RESOLUTION[1] / 2 - 20, 450, 40),
            pygame.Rect(50, constants.RESOLUTION[1] / 2 + 80, 450, 40)
        ]
        
        # Run the parent constructor and update the screen.
        super().__init__(self.buttonGroup, constants.BACKGROUND_COLOUR)

        # Add labels to the textboxes and add those to the changed areas too.
        fontImage = constants.MEDIUMFONT.render("Player 1 (black)'s name:", True, pygame.Color("black")).convert_alpha()
        pygame.display.get_surface().blit(fontImage, (50, constants.RESOLUTION[1] / 2 - 50))
        changedAreas.append(pygame.Rect(50, constants.RESOLUTION[1] / 2 - 50, fontImage.get_width(), fontImage.get_height()))

        fontImage = constants.MEDIUMFONT.render("Player 2 (white)'s name:", True, pygame.Color("black")).convert_alpha()
        pygame.display.get_surface().blit(fontImage, (50, constants.RESOLUTION[1] / 2 + 50))
        changedAreas.append(pygame.Rect(50, constants.RESOLUTION[1] / 2 + 50, fontImage.get_width(), fontImage.get_height()))
        pygame.display.update(changedAreas)

    def update(self, changedRects = [None]):
        for textbox in self.textboxGroup:
            textbox.draw()
            changedRects.append(textbox.rect)
        super().update(changedRects)
    
    def click(self):
        for textbox in self.textboxGroup:
            # If the mouse is currently over the textbox, the user wants to focus it.
            if textbox.collide(pygame.mouse.get_pos()):
                textbox.active = True
            else:
                result = super().click()
                # If the result is nothing, then the textbox should be unfocussed.
                if result == "":
                    textbox.active = False
                # Otherwise, the appropriate scene should be loaded.
                else:
                    return result

    def keyPress(self, e):
        for textbox in self.textboxGroup:
            if textbox.active:
                textbox.keyPress(e)

class TextBox(Button):
    def __init__(self, x, y, width, height, bdrWidth, bgColour, bdrInactiveColour, bdrActiveColour, fontToUse, txtColour):
        super().__init__(x, y, width, height, bdrWidth, bgColour, bdrInactiveColour, bdrActiveColour, "", fontToUse, txtColour)
        self.active = False
        self.textSurface = fontToUse.render(self.text, True, self.fontColour)

    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.active = True
    
    def keyPress(self, event):
        # Only process the key if the textbox is active.
        if self.active == True:
            # If backspace was pressed, delete the last character.
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                if len(self.text) < 30:
                    self.text += event.unicode
            self.draw()
