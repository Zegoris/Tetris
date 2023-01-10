import pygame
import json
from random import choice, randint
import time
import os
import csv

pygame.init()
pygame.mixer.init()

cursor_group = pygame.sprite.Group()  # Creating group of sprites
pygame.mouse.set_visible(False)
runm = 0


def load_image(name):
    fullname = os.path.join('sprites', name)  # Create a path to a picture file
    image = pygame.image.load(fullname)
    return image


class Cursor(pygame.sprite.Sprite):  # Class of the cursor
    def __init__(self, image):
        super().__init__(cursor_group)
        self.image = load_image(image)  # Set image jf the sprite
        self.rect = self.image.get_rect()  # Set size of the sprite


cursor = Cursor('cursor.png')  # Initialization of the cursor


class Game_Over:
    def __init__(self, score):
        global cursor
        self.score = score
        self.size = self.width, self.height = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        self.running = True
        with open("settings.json") as file:
            data = json.load(file)
            self.music = data['Music']
            self.sounds = data['Sounds']
            self.theme = data['DarkTheme']
            self.lightTheme = tuple(data['Color']['Light'])
            self.darkTheme = tuple(data['Color']['Dark'])
            self.user = data['NickName']
        if self.theme:
            self.themeColor = self.lightTheme
        else:
            self.themeColor = self.darkTheme
        self.screen.fill(self.themeColor)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.click(event.pos):
                        self.running = False

            self.screen.fill(self.themeColor)
            self.render()

    def click(self, pos):
        # If Mouse Pos in HitBox True
        if self.button_HitBox_x - 10 <= pos[0] <= self.button_HitBox_sizeX\
                and self.button_HitBox_y - 12 <= pos[1] <= self.button_HitBox_sizeY:
            return True
        return False

    def info(self): # Drawing information about user and score
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font_score = pygame.font.SysFont('symbol', 45)
        score = '0' * (5 - len(str(self.score))) + str(self.score)
        text_score = font_score.render(score, True, fontColor)
        text_score_x = self.width - 290
        text_score_y = 260

        font_go = pygame.font.SysFont('arial', 45)
        text_go = font_go.render('GAME OVER', True, fontColor)
        text_go_x = self.width - 440
        text_go_y = 25

        font_Score = pygame.font.SysFont('arial', 45)
        text_Score = font_Score.render('Score:', True, fontColor)
        text_Score_x = self.width - 430
        text_Score_y = 250

        self.screen.blit(text_score, (text_score_x, text_score_y))
        self.screen.blit(text_go, (text_go_x, text_go_y))
        self.screen.blit(text_Score, (text_Score_x, text_Score_y))

    def button(self): # Drawing exit button
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font = pygame.font.SysFont('arial', 30)
        text = font.render('Continue', True, fontColor)
        text_x = self.width - 365
        text_y = 400
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, fontColor, (text_x - 15, text_y - 15,
                                                     text.get_width() + 30, text.get_height() + 30), 3)
        # HitBox of a button "Continue"
        self.button_HitBox_x = text_x - 10
        self.button_HitBox_y = text_y - 5
        self.button_HitBox_sizeX = text_x + 130
        self.button_HitBox_sizeY = text_y + 50

    def render(self):
        if self.theme:
            borderColor = pygame.Color('white')
        else:
            borderColor = pygame.Color((30, 61, 89))
        self.info() # Information about user and score
        self.button() # Exit button

        if pygame.mouse.get_focused(): # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()


Game_Over(25)