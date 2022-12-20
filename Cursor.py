import pygame
import os

pygame.init()
pygame.mixer.init()
all_sprites = pygame.sprite.Group()  # Creating group of sprites
pygame.mouse.set_visible(False)

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)  # Create a path to a picture file
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Cursor(pygame.sprite.Sprite):  # Class of the cursor
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = load_image(image)  # Set image jf the sprite
        self.rect = self.image.get_rect()  # Set size of the sprite
