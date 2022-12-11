import pygame
import json
from random import choice, randint
import time
import os

pygame.init()
pygame.mixer.init()


class Cursor:
    def __init__(self, image):
        self.size = self.width, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)
        self.all_sprites = pygame.sprite.Group() # Creating group of sprites
        self.sprite = pygame.sprite.Sprite() # Creating a sprite
        self.sprite.image = self.load_image(image) # Set image jf the sprite
        self.sprite.rect = self.sprite.image.get_rect() # Set size of the sprite
        self.all_sprites.add(self.sprite)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                self.sprite.rect.x, self.sprite.rect.y = pygame.mouse.get_pos() # Set the position of the cursor
                self.screen.fill('black')
                self.all_sprites.draw(self.screen)
            else:
                self.screen.fill('black')
            pygame.display.flip()

    def load_image(self, name, colorkey=None):
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


Cursor('cursor.png')
