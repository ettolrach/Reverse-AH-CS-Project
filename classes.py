import pygame, os

class Disc(pygame.sprite.Sprite):
    def __init__(self, isWhiteInitially, xPos, yPos, pathToImage = None):
        pygame.sprite.Sprite.__init__(self)
        self.isWhite = isWhiteInitially
        self.image = pygame.Surface([78,78])
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos

        if isWhiteInitially == True:
            self.image = pygame.image.load(os.path.join("sprites", "blackDisc.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join("sprites", "whiteDisc.png")).convert_alpha()
    
    def change_colour(self):
        if self.isWhite == True:
            self.image = pygame.image.load(os.path.join("sprites", "blackDisc.png")).convert_alpha()
            self.isWhite = False
        else:
            self.image = pygame.image.load(os.path.join("sprites", "whiteDisc.png")).convert_alpha()
            self.isWhite = True
