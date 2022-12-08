import pygame
import json
pygame.init()
#

# Мяу :)

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

        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load('Music/MeryCristmasTrap_fon.mp3')
        if self.Music:
            pygame.mixer.music.play()

        self.sound_push_button = pygame.mixer.Sound('Sounds/push_button.mp3')


        # HitBox
        self.ChB_Music_posX = 175
        self.ChB_Music_posY = 110
        self.ChB_MusicHitBox_X = self.ChB_Music_posX + 65
        self.ChB_MusicHitBox_Y = self.ChB_Music_posY + 20

        self.ChB_Sound_posX = 275
        self.ChB_Sound_posY = 110
        self.ChB_SoundHitBox_X = self.ChB_Sound_posX + 65
        self.ChB_SoundHitBox_Y = self.ChB_Sound_posY + 20

        self.ChB_Theme_posX = self.width // 2 - 118 // 2
        self.ChB_Theme_posY = 150
        self.ChB_ThemeHitBox_X = self.ChB_Theme_posX + 65
        self.ChB_ThemeHitBox_Y = self.ChB_Theme_posY + 20




        self.draw()  # draw all
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:               # Stop Programm
                    running = False                         # write class of MainWind? for restart game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)

    # Change settings
    def click(self, pos):
        if self.ChB_MusicHitBox_X >= pos[0] >= self.ChB_Music_posX - 30 and self.ChB_MusicHitBox_Y >= pos[1] >= self.ChB_Music_posY - 5:
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
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.pause()
                data["Music"] = True if self.Music else False
                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)

        elif self.ChB_SoundHitBox_X >= pos[0] >= self.ChB_Sound_posX - 30 and self.ChB_SoundHitBox_Y >= pos[1] >= self.ChB_Sound_posY - 5:
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

        elif self.ChB_ThemeHitBox_X >= pos[0] >= self.ChB_Theme_posX - 30 and self.ChB_ThemeHitBox_Y >= pos[1] >= self.ChB_Theme_posY - 5:
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


Settings_Window()
