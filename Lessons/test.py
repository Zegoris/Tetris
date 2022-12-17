import pygame
import os
import sys
import random

pygame.init()

BLACK = (255, 255, 255)
W, H = 1000, 570

sc = pygame.display.set_mode((W, H))
sc.fill((255, 255, 255))
clock = pygame.time.Clock()
FPS = 60

all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


speed = 10
bomb_image = load_image("bomb.png", -1)

for i in range(50):
    # можно сразу создавать спрайты с указанием группы
    bomb = pygame.sprite.Sprite(all_sprites)
    bomb.image = bomb_image
    bomb.rect = bomb.image.get_rect()

    # задаём случайное местоположение бомбочке
    bomb.rect.x = random.randrange(W)
    bomb.rect.y = random.randrange(H)

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    all_sprites.draw(sc)
    pygame.display.flip()
    clock.tick(FPS)

