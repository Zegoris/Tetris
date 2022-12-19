import pygame
import json
import random
import os

runm = 0

class MainWindow():
    def __init__(self):
        pygame.init()  # init pygame
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        running = True
        global runm
        self.runM = runm

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
        pygame.mixer.music.load("Data/Music/" + str(random.choice(os.listdir("Data/Music"))))
        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')

        # Play Music
        if self.Music:
            pygame.mixer.music.play()

        self.draw()  # draw all

        # Staff
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)

    # Draw all in screen
    def draw(self):
        self.screen.fill(self.TextColor)        # Fill display color
        pygame.display.flip()

        # Title "Tetris"
        font = pygame.font.Font(None, 60)
        text = font.render("T_E_T_R_I_S", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 40
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                               text.get_width() + 20, text.get_height() + 20), 6)


        # Btn "Play"
        font = pygame.font.Font(None, 60)
        text = font.render("    PLAY     ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 170
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        # HitBox of Btn "Play"
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
        # HitBox of Btn "Play"
        self.BtnSett_HuitBox_X = text_x
        self.BtnSett_HuitBox_Y = text_y
        self.BtnSett_HuitBox_XSize = text_x + 500
        self.BtnSett_HuitBox_YSize = text_y + 50

        # Draw Changes
        pygame.display.flip()

    # CLick Operation
    def click(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()

        # If Mouse Pos in HitBox's ->
        if self.BtnPlay_HuitBox_X <= pos[0] <= self.BtnPlay_HuitBox_XSize and self.BtnPlay_HuitBox_Y <= pos[1] <= self.BtnPlay_HuitBox_YSize:
            Levels_Window()
        elif self.BtnSett_HuitBox_X <= pos[0] <= self.BtnSett_HuitBox_XSize and self.BtnSett_HuitBox_Y <= pos[1] <= self.BtnSett_HuitBox_YSize:
            global runm
            runm = 1
            # Open SettingsWindow
            Settings_Window()


class Settings_Window():
    def __init__(self):
        pygame.init()       # init pygame
        self.size = self.width, self.height = 500, 700      # Window Size
        self.screen = pygame.display.set_mode(self.size)    # Screen Setting
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

        # Play Music
        if self.Music:
            pygame.mixer.music.unpause()
        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')


        # HitBox
        # Chb "Music"
        self.ChB_Music_posX = 175
        self.ChB_Music_posY = 110
        self.ChB_MusicHitBox_X = self.ChB_Music_posX + 65
        self.ChB_MusicHitBox_Y = self.ChB_Music_posY + 20
        # Chb "Sounds"
        self.ChB_Sound_posX = 275
        self.ChB_Sound_posY = 110
        self.ChB_SoundHitBox_X = self.ChB_Sound_posX + 65
        self.ChB_SoundHitBox_Y = self.ChB_Sound_posY + 20
        # Chb "Theme"
        self.ChB_Theme_posX = self.width // 2 - 118 // 2
        self.ChB_Theme_posY = 150
        self.ChB_ThemeHitBox_X = self.ChB_Theme_posX + 65
        self.ChB_ThemeHitBox_Y = self.ChB_Theme_posY + 20

        self.draw()  # draw all
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:               # Stop Program
                    # play sound if "settings" close
                    if self.Sound:
                        pygame.mixer.music.pause()
                        self.sound_push_button.play()
                        if self.Music:
                            pygame.mixer.music.unpause()

                    MainWindow()    # Opne MainWindow
                    running = False                         # write class of MainWind? for restart game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)


    # Change settings
    def click(self, pos):
        # If Mouse Pos in HitBox "Music"
        if self.ChB_MusicHitBox_X >= pos[0] >= self.ChB_Music_posX - 30 and self.ChB_MusicHitBox_Y >= pos[1] >= self.ChB_Music_posY - 5:
            # Play Sounds
            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()

            # Open Sett_file and replace "Music"
            with open("settings.json") as file:
                data = json.load(file)
                self.Music = False if self.Music else True
                if self.Music:
                    pygame.mixer.music.load("Data/Music/" + str(random.choice(os.listdir("Data/Music"))))
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.pause()
                data["Music"] = True if self.Music else False
                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)

        # If Mouse Pos in HitBox "Sound"
        elif self.ChB_SoundHitBox_X >= pos[0] >= self.ChB_Sound_posX - 30 and self.ChB_SoundHitBox_Y >= pos[1] >= self.ChB_Sound_posY - 5:
            # Play Sounds
            if not self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()

            # Open Sett_file and replace "Sound"
            with open("settings.json") as file:
                data = json.load(file)
                self.Sound = False if self.Sound else True
                data["Sounds"] = True if self.Sound else False
                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)

        # If Mouse Pos in HitBox "Theme"
        elif self.ChB_ThemeHitBox_X >= pos[0] >= self.ChB_Theme_posX - 30 and self.ChB_ThemeHitBox_Y >= pos[1] >= self.ChB_Theme_posY - 5:
            # Play Sounds
            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()

            # Open Sett_file and replace "Theme"
            with open("settings.json") as file:
                data = json.load(file)
                if self.DarkTheme:
                    self.TextColor = tuple(data["Color"]["Dark"])
                    self.BgColor = tuple(data["Color"]["Light"])
                else:
                    self.TextColor = tuple(data["Color"]["Light"])
                    self.BgColor = tuple(data["Color"]["Dark"])
                self.DarkTheme = False if self.DarkTheme else True
                data["DarkTheme"] = True if self.DarkTheme else False

                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)

        self.draw()

    # Draw on windwo: Title, other sett.
    def draw(self):
        self.screen.fill(self.TextColor)                             # BackGround color

        # draw title
        font = pygame.font.Font(None, 50)
        text = font.render("GAME SETTINGS", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 40
        self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()


        # draw ChB "Music"
        # draw text
        font = pygame.font.Font(None, 30)
        text = font.render("Music", True, self.BgColor)
        text_x = self.ChB_Music_posX
        text_y = self.ChB_Music_posY
        self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.Music:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))
            pygame.display.flip()
        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.display.flip()


        # draw ChB "Sound"
        # draw text
        font = pygame.font.Font(None, 30)
        text = font.render("Sounds", True, self.BgColor)
        text_x = self.ChB_Sound_posX
        text_y = self.ChB_Sound_posY
        self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.Sound:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))
            pygame.display.flip()
        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.display.flip()


        # draw ChB "Theme"
        # draw text
        font = pygame.font.Font(None, 30)
        text = font.render("Dark Theme", True, self.BgColor)
        text_x = self.ChB_Theme_posX
        text_y = self.ChB_Theme_posY
        self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.DarkTheme:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))
            pygame.display.flip()
        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.display.flip()


class Levels_Window():
    def __init__(self):
        pygame.init()  # init pygame
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        running = True
        global runm
        self.runM = runm

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
        pygame.mixer.music.load("Data/Music/" + str(random.choice(os.listdir("Data/Music"))))
        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')

        # Play Music
        if self.Music:
            pygame.mixer.music.play()

        self.draw()  # draw all

        # Staff
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #elf.click(event.pos)
                    pass

    def draw(self):
        self.screen.fill(self.TextColor)        # Fill display color
        pygame.display.flip()

MainWindow()