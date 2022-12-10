import pygame
import json
import random
import os
import SettingsWindow


class MainWindow():
    def __init__(self):
        pygame.init()  # init pygame
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        running = True

        # open setting.json and take var
        with open("settings.json") as file:
            data = json.load(file)
            self.Music = data["Music"]
            self.Sound = data["Sounds"]
            self.DarkTheme = data["DarkTheme"]
            if self.DarkTheme:
                self.TextColor = tuple(data["Color"]["Light"])
                self.BgColor = tuple(data["Color"]["Dark"])
            else:
                self.TextColor = tuple(data["Color"]["Dark"])
                self.BgColor = tuple(data["Color"]["Light"])



        # Music
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load("Music/" + str(random.choice(os.listdir("Music"))))
        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Sounds/push_button.mp3')

        if self.Music:
            pygame.mixer.music.play()

        self.draw()  # draw all

        # Staff
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    running = False  # write class of MainWind? for restart game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)

    def draw(self):
        self.screen.fill(self.TextColor)
        pygame.display.flip()

        # Title
        font = pygame.font.Font(None, 60)
        text = font.render("T_E_T_R_I_S", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 40
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                               text.get_width() + 20, text.get_height() + 20), 6)

        # Btn Play
        font = pygame.font.Font(None, 60)
        text = font.render("    PLAY     ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 170
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        self.BtnPlay_HuitBox_X = text_x
        self.BtnPlay_HuitBox_Y = text_y
        self.BtnPlay_HuitBox_XSize = text_x + 500
        self.BtnPlay_HuitBox_YSize = text_y + 50

        # Btn Sett
        font = pygame.font.Font(None, 60)
        text = font.render(" SETTINGS ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 250
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        self.BtnSett_HuitBox_X = text_x
        self.BtnSett_HuitBox_Y = text_y
        self.BtnSett_HuitBox_XSize = text_x + 500
        self.BtnSett_HuitBox_YSize = text_y + 50


        pygame.display.flip()

    def click(self, pos):
        if self.BtnPlay_HuitBox_X <= pos[0] <= self.BtnPlay_HuitBox_XSize and self.BtnPlay_HuitBox_Y <= pos[1] <= self.BtnPlay_HuitBox_YSize:
            print("TEST PLAY")
        elif self.BtnSett_HuitBox_X <= pos[0] <= self.BtnSett_HuitBox_XSize and self.BtnSett_HuitBox_Y <= pos[1] <= self.BtnSett_HuitBox_YSize:
            SettingsWindow.Settings_Window()


MainWindow()