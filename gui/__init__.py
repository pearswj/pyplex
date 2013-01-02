import os 
import pygame.image, pygame.display

class BackgroundImage:
    #todo, remove hardcoded
    def __init__(self, picture):
        # pygame.init()
        pictureFile = open(os.path.join(os.path.dirname(__file__), picture));
        self.picture = pygame.image.load(pictureFile)
        self.picture = pygame.transform.scale(self.picture,(1280,1024))

    def set(self):
        # pygame.mouse.set_visible(False)
        pygame.display.set_mode(self.picture.get_size())
        main_surface = pygame.display.get_surface()
        main_surface.blit(self.picture, (0, 0))
        pygame.display.update()


