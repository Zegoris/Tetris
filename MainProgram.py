import pygame
import json
from random import choice, randint
import time
import os
import csv
# Egor
pygame.init()
pygame.mixer.init()

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("Data/Music/" + str(choice(os.listdir("Data/Music"))))
with open("settings.json") as file:
    d = json.load(file)
    music = d['Music']
if music:
    pygame.mixer.music.play(loops=-1)

cursor_group = pygame.sprite.Group()  # Creating group of sprites
pygame.mouse.set_visible(False)
nick = 0

def load_image(name):
    fullname = os.path.join('Data/Sprites', name)  # Create a path to a picture file
    image = pygame.image.load(fullname)
    return image


def write_records(user, gm, score):
    yes = False
    with open('records.csv', encoding="utf8") as csvf:
        reader = csv.reader(csvf, delimiter=',', quotechar='"')
        reader = list(reader)
    if len(reader) >= 11:
        reader = reader[:12]
    reader = sorted(reader[1:], reverse=True, key=lambda x: int(x[1]) + int(x[2]))
    reader.insert(0, ['user', 'first_gm', 'second_gm'])
    os.remove('records.csv')
    for number, item in enumerate(reader[1:]):
        if user in item:
            yes = True
            if gm == 1:
                if int(item[1]) < score:
                    reader[number + 1] = [user, score, item[2]]
            elif gm == 2:
                if int(item[2]) < score:
                    reader[number + 1] = [user, item[1], score]
            break
    if not yes:
        if gm == 1:
            reader.append([user, score, '0'])
        elif gm == 2:
            reader.append([user, '0', score])
    reader = sorted(reader[1:], reverse=True, key=lambda x: int(x[1]) + int(x[2]))
    reader.insert(0, ['user', 'first_gm', 'second_gm'])

    with open('records.csv', 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerows(reader)


def read_records():
    with open('records.csv', encoding="utf8") as csvf:
        reader = csv.reader(csvf, delimiter=',', quotechar='"')
        reader = list(reader)[1:]
    reader = sorted(reader,reverse=True, key=lambda x: int(x[1]) + int(x[2]))
    answer = []
    for i in reader:
        n = 0
        for j in i[1:]:
            n += int(j)
        answer.append([i[0], str(n)])
    return answer


class Cursor(pygame.sprite.Sprite):  # Class of the cursor
    def __init__(self, image):
        super().__init__(cursor_group)
        self.image = load_image(image)  # Set image jf the sprite
        self.rect = self.image.get_rect()  # Set size of the sprite


cursor = Cursor('cursor.png')  # Initialization of the cursor


class Game_Over:
    def __init__(self, score, gm):
        global cursor
        self.score = score
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting

        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')
        pygame.display.set_caption('Game')
        self.running = True
        with open("settings.json") as file:
            data = json.load(file)
            self.Music = data['Music']
            self.Sound = data['Sounds']
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
                    if self.quit(event.pos):
                        self.running = False
                        MainWindow()
                    if self.click(event.pos):
                        self.running = False
                        if gm == 1:
                            First_GM()
                        elif gm == 2:
                            Second_GM()

            self.screen.fill(self.themeColor)
            self.render()

    def quit(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()
        # If Mouse Pos in HitBox True
        if self.button_HitBoxC_x - 10 <= pos[0] <= self.button_HitBoxC_sizeX\
                and self.button_HitBoxC_y - 12 <= pos[1] <= self.button_HitBoxC_sizeY:
            return True
        return False

    def click(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()
        if self.button_HitBox_x - 10 <= pos[0] <= self.button_HitBox_sizeX\
                and self.button_HitBox_y - 12 <= pos[1] <= self.button_HitBox_sizeY:
            return True
        return False

    def info(self): # Drawing information about user and score
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font_score = pygame.font.Font('Data/Fonts/asymbols.ttf', 45)
        score = '0' * (5 - len(str(self.score))) + str(self.score)
        text_score = font_score.render(score, True, fontColor)
        text_score_x = self.width - 235
        text_score_y = 240

        font_go = pygame.font.SysFont('arial', 55)
        text_go = font_go.render('GAME OVER', True, fontColor)
        text_go_x = self.width - 414
        text_go_y = 25

        font_Score = pygame.font.SysFont('arial', 45)
        text_Score = font_Score.render('Score:', True, fontColor)
        text_Score_x = self.width - 380
        text_Score_y = 230

        self.screen.blit(text_score, (text_score_x, text_score_y))
        self.screen.blit(text_go, (text_go_x, text_go_y))
        self.screen.blit(text_Score, (text_Score_x, text_Score_y))

    def button(self): # Drawing exit button
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font = pygame.font.SysFont('arial', 30)
        text = font.render('Replay', True, fontColor)
        text_x = self.width - 310
        text_y = 360
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, fontColor, (text_x - 15, text_y - 15,
                                                     text.get_width() + 30, text.get_height() + 30), 3)
        # HitBox of a button "Replay"
        self.button_HitBox_x = text_x - 10
        self.button_HitBox_y = text_y - 5
        self.button_HitBox_sizeX = text_x + 130
        self.button_HitBox_sizeY = text_y + 50

        font = pygame.font.SysFont('arial', 30)
        text = font.render('Continue', True, fontColor)
        text_x = self.width - 320
        text_y = 440
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, fontColor, (text_x - 15, text_y - 15,
                                                  text.get_width() + 30, text.get_height() + 30), 3)
        # HitBox of a button "Continue"
        self.button_HitBoxC_x = text_x - 10
        self.button_HitBoxC_y = text_y - 5
        self.button_HitBoxC_sizeX = text_x + 130
        self.button_HitBoxC_sizeY = text_y + 50

    def render(self):
        self.info() # Information about user and score
        self.button() # Exit button

        if pygame.mouse.get_focused(): # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()


class Board:  # General class for game modes
    def __init__(self, screen, width, height, game_mode):
        global cursor
        pygame.display.set_caption('Game')
        self.tetraminesW, self.tetraminesH = 5, 5
        self.gm = game_mode
        self.tetramines = {'S': [['ooooo',  # Game tetramines
                                  'ooooo',
                                  'ooxxo',
                                  'oxxoo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'ooxxo',
                                  'oooxo',
                                  'ooooo']],
                           'Z': [['ooooo',
                                  'ooooo',
                                  'oxxoo',
                                  'ooxxo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'oxxoo',
                                  'oxooo',
                                  'ooooo']],
                           'J': [['ooooo',
                                  'oxooo',
                                  'oxxxo',
                                  'ooooo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxxo',
                                  'ooxoo',
                                  'ooxoo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooooo',
                                  'oxxxo',
                                  'oooxo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'ooxoo',
                                  'oxxoo',
                                  'ooooo']],
                           'L': [['ooooo',
                                  'oooxo',
                                  'oxxxo',
                                  'ooooo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'ooxoo',
                                  'ooxxo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooooo',
                                  'oxxxo',
                                  'oxooo',
                                  'ooooo'],
                                 ['ooooo',
                                  'oxxoo',
                                  'ooxoo',
                                  'ooxoo',
                                  'ooooo']],
                           'I': [['ooxoo',
                                  'ooxoo',
                                  'ooxoo',
                                  'ooxoo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooooo',
                                  'xxxxo',
                                  'ooooo',
                                  'ooooo']],
                           'O': [['ooooo',
                                  'ooooo',
                                  'oxxoo',
                                  'oxxoo',
                                  'ooooo']],
                           'T': [['ooooo',
                                  'ooxoo',
                                  'oxxxo',
                                  'ooooo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'ooxxo',
                                  'ooxoo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooooo',
                                  'oxxxo',
                                  'ooxoo',
                                  'ooooo'],
                                 ['ooooo',
                                  'ooxoo',
                                  'oxxoo',
                                  'ooxoo',
                                  'ooooo']]}
        self.size = self.widthW, self.heightW = 600, 750  # Window Size
        self.running = True

        self.width = width
        self.height = height
        self.board = [['o'] * height for _ in range(width)]  # Matrix of values of painted cells
        self.cell_size = 24
        self.score = 0
        self.screen = screen
        with open("settings.json") as file:
            data = json.load(file)
            self.Music = data['Music']
            self.Sound = data['Sounds']
            self.theme = data['DarkTheme']
            self.lightTheme = tuple(data['Color']['Light'])
            self.darkTheme = tuple(data['Color']['Dark'])
            self.user = data['NickName']
            self.form = data['Form']
            self.color = data['Colors']
        self.colors = {'Random': {'light': ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30)),
                                  'dark': ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))},
                       'Girls': {'light': ((167, 0, 179), (157, 28, 166), (243, 82, 255), (183, 0, 255)),
                                 'dark': ((122, 3, 130), (70, 21, 74), (119, 30, 125), (85, 0, 255))},
                       'Forest': {'light': ((0, 168, 81), (15, 196, 2), (65, 184, 57), (58, 133, 77)),
                                  'dark': ((0, 105, 51), (10, 143, 0), (32, 115, 26), (8, 38, 15))}
                       }
        if self.theme:
            self.themeColor = self.lightTheme
        else:
            self.themeColor = self.darkTheme

        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')
        self.screen.fill(self.themeColor)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.last_down = time.time()
        self.last_side = time.time()
        self.last_fall = time.time()
        self.down = False  # Is it possible to move to the down
        self.left = False  # Is it possible to move to the left
        self.right = False  # Is it possible to move to the right
        self.fall_speed = self.static()
        self.fallingTetramine = self.newTetramine()
        self.nextTetramine = self.newTetramine()

        while self.running:
            if self.fallingTetramine is None:  # If there are no falling tetramine, we generate a new one
                self.fallingTetramine = self.nextTetramine
                self.nextTetramine = self.newTetramine()
                self.last_fall = time.time()
                if not self.check(self.fallingTetramine):
                    write_records(self.user, self.gm, self.score)
                    self.running = False  # If there is no free space on the playing field - the game is over, FINAL WINDOW
                    Game_Over(self.score, self.gm)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.quit(event.pos):
                        write_records(self.user, self.gm, self.score)
                        self.running = False
                        Game_Over(self.score, self.gm)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.left = False
                    if event.key == pygame.K_RIGHT:
                        self.right = False
                    if event.key == pygame.K_DOWN:
                        self.down = False
                if event.type == pygame.KEYDOWN:  # Moving the tetramine to the right and left
                    if event.key == pygame.K_LEFT and self.check(self.fallingTetramine, x0=-1):
                        self.fallingTetramine['x'] -= 1
                        self.left = True
                        self.right = False
                        self.last_side = time.time()
                    if event.key == pygame.K_RIGHT and self.check(self.fallingTetramine, x0=1):
                        self.fallingTetramine['x'] += 1
                        self.right = True
                        self.left = False
                        self.last_side = time.time()
                    if event.key == pygame.K_UP:  # Rotate the tetramine if there is room
                        self.fallingTetramine['rotation'] = (self.fallingTetramine['rotation'] + 1) \
                                                            % len(self.tetramines[self.fallingTetramine['shape']])
                        if not self.check(self.fallingTetramine):
                            self.fallingTetramine['rotation'] = (self.fallingTetramine['rotation'] - 1) \
                                                                % len(self.tetramines[self.fallingTetramine['shape']])
                    if event.key == pygame.K_DOWN:  # Speed up the fall of the tetramine
                        self.down = True
                        if self.check(self.fallingTetramine, y0=1):
                            self.fallingTetramine['y'] += 1
                        self.last_down = time.time()
                    if event.key == pygame.K_SPACE:  # Instant reset of the tetramine
                        self.down = False
                        self.left = False
                        self.right = False
                        for i in range(1, self.height):
                            end = i - 1
                            if not self.check(self.fallingTetramine, y0=i):
                                break
                        self.fallingTetramine['y'] += end
                        self.score += 3
            # Controlling the fall of the tetramine while holding down the keys
            if (self.left or self.right) and time.time() - self.last_side > 0.1:
                if self.left and self.check(self.fallingTetramine, x0=-1):
                    self.fallingTetramine['x'] -= 1
                elif self.right and self.check(self.fallingTetramine, x0=1):
                    self.fallingTetramine['x'] += 1
                self.last_side = time.time()
            if self.down and time.time() - self.last_down > 0.1 \
                    and self.check(self.fallingTetramine, y0=1):
                self.fallingTetramine['y'] += 1
                self.last_down = time.time()
            if time.time() - self.last_fall > self.fall_speed:  # Free fall of the tetramine
                if not self.check(self.fallingTetramine, y0=1):
                    self.add(self.fallingTetramine)  # The tetramine has landed, add it to the contents of the board
                    self.score += self.clearCompleted() * 300 if self.score <= 99999 else 99999
                    self.fall_speed = self.static()
                    self.fallingTetramine = None
                else:  # The tetramine hasn't landed yet, we keep moving down
                    self.fallingTetramine['y'] += 1
                    self.last_fall = time.time()
            self.screen.fill(self.themeColor)
            self.render()
            self.clock.tick(self.fps)

    def isCompleted(self, y):  # Check the presence of fully filled rows
        for x in range(self.width):
            if self.board[x][y] == 'o':
                return False
        return True

    def clearCompleted(self):  # Removing filled rows and shifting the top rows down
        removed_lines = 0
        y0 = self.height - 1
        while y0 >= 0:
            if self.isCompleted(y0):
                for y in range(y0, 0, -1):
                    for x in range(self.width):
                        self.board[x][y] = self.board[x][y - 1]
                for x in range(self.width):
                    self.board[x][0] = 'o'
                removed_lines += 1
            else:
                y0 -= 1
        return removed_lines

    def quit(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()

        # If Mouse Pos in HitBox True
        if self.button_HitBox_x - 10 <= pos[0] <= self.button_HitBox_sizeX\
                and self.button_HitBox_y - 12 <= pos[1] <= self.button_HitBox_sizeY:
            return True
        return False

    def check(self, tetramine, x0=0, y0=0):  # Checks if the tetramine is within the board boundaries without colliding with other tetramines
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                above_board = y + tetramine['y'] + y0 < 0
                if above_board or self.tetramines[tetramine['shape']][tetramine['rotation']][y][x] == 'o':
                    continue

                if not self.inBoard(x + tetramine['x'] + x0, y + tetramine['y'] + y0):
                    return False

                if self.board[x + tetramine['x'] + x0][y + tetramine['y'] + y0] != 'o':
                    return False
        return True

    def inBoard(self, x, y):
        return self.width > x >= 0 and 0 <= y < self.height

    def add(self, tetramine):
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if self.tetramines[tetramine['shape']][tetramine['rotation']][y][x] != 'o':
                    self.board[x + tetramine['x']][y + tetramine['y']] = tetramine['color']

    def static(self): # Calculating game's speed
        return 0.2

    def coords(self, x, y):
        return (10 + (x * self.cell_size)), \
            (5 + (y * self.cell_size))

    def newTetramine(self):  # Returns a new tetramine with a random color and rotation angle
        shape = choice(list(self.tetramines.keys()))
        return {'shape': shape,
                'rotation': randint(0, len(self.tetramines[shape]) - 1),
                'x': int(self.width / 2) - int(self.tetraminesW / 2),
                'y': -2,
                'color': randint(0, len(self.colors[self.color]['dark']) - 1)}

    def drawBlock(self, block_x, block_y, color, size, x=None, y=None):  # Drawing the square blocks that make up the tetramines
        if color == 'o':
            return

        if x is None and y is None:
            x, y = self.coords(block_x, block_y)
        if self.form == 'Rectangles':
            pygame.draw.rect(self.screen, self.colors[self.color]['dark'][color],
                             (x + 1, y + 1, size - 1,
                              size - 1), 0, 3)
            pygame.draw.rect(self.screen, self.colors[self.color]['light'][color],
                             (x + 1, y + 1, size - 4,
                              size - 4), 0, 3)
            pygame.draw.circle(self.screen, self.colors[self.color]['dark'][color],
                               (x + size / 2,
                                y + size / 2), size / 4.5)
        elif self.form == 'Rectangle':
            pygame.draw.rect(self.screen, self.colors[self.color]['dark'][color],
                             (x + 1, y + 1, size,
                              size), 0)
            pygame.draw.rect(self.screen, self.colors[self.color]['light'][color],
                             (x + 1, y + 1, size - 3,
                              size - 3), 0)
            pygame.draw.circle(self.screen, self.colors[self.color]['dark'][color],
                               (x + size / 2,
                                y + size / 2), size / 4.5)
        elif self.form == 'Circle':
            pygame.draw.circle(self.screen, self.colors[self.color]['dark'][color],
                               (x + size / 2,
                                y + size / 2), size / 2)
            pygame.draw.circle(self.screen, self.colors[self.color]['light'][color],
                               (x + size / 2.2,
                                y + size / 2.2), size / 2.2)

    def drawTetramine(self, tetramine, size, x0=None, y0=None):
        tetramineDraw = self.tetramines[tetramine['shape']][tetramine['rotation']]
        if x0 is None and y0 is None:
            x0, y0 = self.coords(tetramine['x'], tetramine['y'])
        # Drawing tetramine elements
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if tetramineDraw[y][x] != 'o':
                    self.drawBlock(None, None, tetramine['color'], size, x0 + (x * size),
                                   y0 + (y * size))

    def info(self): # Drawing information about user and score
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font_score = pygame.font.Font('Data/Fonts/asymbols.ttf', 45)
        score = '0' * (5 - len(str(self.score))) + str(self.score)
        text_score = font_score.render(score, True, fontColor)
        text_score_x = self.widthW - 170
        text_score_y = 300

        font_user = pygame.font.SysFont('arial', 30)
        text_user = font_user.render(self.user, True, fontColor)
        text_user_x = self.widthW - 170
        text_user_y = 25
        self.screen.blit(text_score, (text_score_x, text_score_y))
        self.screen.blit(text_user, (text_user_x, text_user_y))

    def button(self): # Drawing exit button
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font = pygame.font.SysFont('arial', 20)
        text = font.render('Quit', True, fontColor)
        text_x = self.widthW - 130
        text_y = 670
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, fontColor, (text_x - 15, text_y - 15,
                                                     text.get_width() + 30, text.get_height() + 30), 3)
        # HitBox of a button "Quit"
        self.button_HitBox_x = text_x - 10
        self.button_HitBox_y = text_y - 5
        self.button_HitBox_sizeX = text_x + 45
        self.button_HitBox_sizeY = text_y + 35

    def render(self):
        if self.theme:
            borderColor = pygame.Color('white')
        else:
            borderColor = pygame.Color((30, 61, 89))
        self.info() # Information about user and score
        self.button() # Exit button

        for x in range(self.width):
            for y in range(self.height):
                self.drawBlock(x, y, self.board[x][y], size=self.cell_size)  # Already landed tetramine
        self.drawTetramine(self.nextTetramine, self.cell_size + 10, x0=400, y0=70)  # Preview of the next tetramine

        if self.fallingTetramine is not None:
            self.drawTetramine(self.fallingTetramine, size=self.cell_size)  # Drawing a falling tetramine
        pygame.draw.rect(self.screen, borderColor, (5, 1, 368, 752), 5) # Border of the playing field

        if pygame.mouse.get_focused(): # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()


class First_GM(Board):  # Class of the first game mode
    def __init__(self):
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        Board.__init__(self, self.screen, 15, 31, game_mode=1)


class Second_GM(Board): # Class of the second game mode
    def __init__(self):
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        Board.__init__(self, self.screen, 15, 31, game_mode=2)

    def static(self): # Calculating game's speed
        score = self.score if self.score <= 15000 else 15000
        fall_speed = 0.2 - score / 2500 * 0.02
        return fall_speed

# Maxim
class MainWindow:
    def __init__(self):
        global cursor, nick
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        pygame.display.set_caption('Game')
        self.running = True

        # open setting.json and take var
        with open("settings.json") as file:
            data = json.load(file)
            self.Music = data["Music"]
            self.Sound = data["Sounds"]
            self.DarkTheme = data["DarkTheme"]
            nick = len(data['NickName'])
            if self.DarkTheme:
                self.TextColor = tuple(data["Color"]["Light"])
                self.BgColor = tuple(data["Color"]["Dark"])
            else:
                self.TextColor = tuple(data["Color"]["Dark"])
                self.BgColor = tuple(data["Color"]["Light"])



        # Music

        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')

        # Staff
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
            self.screen.fill(self.TextColor)  # Fill display color
            self.draw()  # draw all

    # Draw all in screen
    def draw(self):

        # Title "Tetris"
        font = pygame.font.Font(None, 60)
        text = font.render("T_E_T_R_I_S", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 40
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                               text.get_width() + 20, text.get_height() + 20), 6)


        # Btn "Play"
        font = pygame.font.SysFont('arial', 45)
        text = font.render("    PLAY     ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 170
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        # HitBox of Btn "Play"
        self.BtnPlay_HitBox_X = text_x - 15
        self.BtnPlay_HitBox_Y = text_y - 10
        self.BtnPlay_HitBox_XSize = text_x + 205
        self.BtnPlay_HitBox_YSize = text_y + 50


        # Btn Sett
        font = pygame.font.SysFont('arial', 45)
        text = font.render(" SETTINGS ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 250
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        # HitBox of Btn "Sett"
        self.BtnSett_HitBox_X = text_x - 15
        self.BtnSett_HitBox_Y = text_y - 10
        self.BtnSett_HitBox_XSize = text_x + 235
        self.BtnSett_HitBox_YSize = text_y + 50

        # Btn "Quit"
        font = pygame.font.SysFont('arial', 25)
        text = font.render("Quit", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 650
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 3)
        self.BtnQ_HitBox_X = text_x - 15
        self.BtnQ_HitBox_Y = text_y - 10
        self.BtnQ_HitBox_XSize = text_x + 235
        self.BtnQ_HitBox_YSize = text_y + 50

        # Btn "Records"
# Egor
        font = pygame.font.SysFont('arial', 45)
        text = font.render(" RECORDS ", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 330
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 2)
        # HitBox of Btn "Records"
        self.BtnR_HitBox_X = text_x - 15
        self.BtnR_HitBox_Y = text_y - 10
        self.BtnR_HitBox_XSize = text_x + 235
        self.BtnR_HitBox_YSize = text_y + 50

        if pygame.mouse.get_focused():  # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)

        # Draw Changes
        pygame.display.flip()
# Maxim
    # CLick Operation
    def click(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()

        # If Mouse Pos in HitBox's ->
        if self.BtnPlay_HitBox_X <= pos[0] <= self.BtnPlay_HitBox_XSize and self.BtnPlay_HitBox_Y <= pos[1]\
                <= self.BtnPlay_HitBox_YSize:
            Levels_Window()
            self.running = False

        elif self.BtnSett_HitBox_X <= pos[0] <= self.BtnSett_HitBox_XSize and self.BtnSett_HitBox_Y <= pos[1]\
                <= self.BtnSett_HitBox_YSize:
            # Open SettingsWindow
            Settings_Window()
            self.running = False
# Egor
        elif self.BtnR_HitBox_X <= pos[0] <= self.BtnR_HitBox_XSize and self.BtnR_HitBox_Y <= pos[1] \
                <= self.BtnR_HitBox_YSize:
            Records()
            self.running = False

        elif self.BtnQ_HitBox_X <= pos[0] <= self.BtnQ_HitBox_XSize and self.BtnQ_HitBox_Y <= pos[1] \
                <= self.BtnQ_HitBox_YSize:

            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()

            self.running = False

# Maxim
class Settings_Window:
    def __init__(self):
        global cursor, nick
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        pygame.display.set_caption('Game')
        self.running = True

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
            self.NickName = data["NickName"]
            self.Form = data["Form"]
            self.Brick_Color = data["Colors"]

        # data of nickname
        self.font = pygame.font.SysFont('arial', 26)
        self.input_box = pygame.Rect(150, 220, 280, 32)
        self.color_inactive = self.BgColor
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        active = False

        # Play Music
        if self.Music:
            pygame.mixer.music.unpause()
        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')
        self.sound_push_keywords = pygame.mixer.Sound('Data/Sounds/push_keywords.mp3')
        self.sound_push_backspace = pygame.mixer.Sound('Data/Sounds/push_backspace.mp3')

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

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Program
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.Sound:
                        self.sound_push_button.play()
                    # NickName
                    if self.input_box.collidepoint(event.pos):
                        # Toggle the active variable.

                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    self.color = self.color_active if active else self.BgColor

                    self.click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if self.Sound:
                        self.sound_push_backspace.play()
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            if self.Sound:
                                self.sound_push_backspace.play()
                            self.NickName = self.NickName[:-1]
                            if nick >= 1:
                                nick -= 1
                            else:
                                nick = 0
                        else:
                            if nick <= 7:
                                nick += 1
                                self.NickName += event.unicode

                        # Open Sett_file and replace "Music"
                        with open("settings.json") as file:
                            data = json.load(file)
                            data["NickName"] = self.NickName
                            with open("settings.json", "w") as file:
                                json.dump(data, file, indent=4)

            self.screen.fill(self.TextColor)  # BackGround color
            self.draw()  # draw all

    # Change settings
    def click(self, pos):
        # If Mouse Pos in HitBox "Music"
        if self.ChB_MusicHitBox_X >= pos[0] >= self.ChB_Music_posX - 30 and self.ChB_MusicHitBox_Y >= pos[
            1] >= self.ChB_Music_posY - 5:
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
                    pygame.mixer.music.load("Data/Music/" + str(choice(os.listdir("Data/Music"))))
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.pause()
                data["Music"] = True if self.Music else False
                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)

        # If Mouse Pos in HitBox "Sound"
        elif self.ChB_SoundHitBox_X >= pos[0] >= self.ChB_Sound_posX - 30 and self.ChB_SoundHitBox_Y >= pos[
            1] >= self.ChB_Sound_posY - 5:
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
        elif self.ChB_ThemeHitBox_X >= pos[0] >= self.ChB_Theme_posX - 30 and self.ChB_ThemeHitBox_Y >= pos[
            1] >= self.ChB_Theme_posY - 5:
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

        # Close levels window
        elif self.BtnQ_HitBox_X <= pos[0] <= self.BtnQ_HitBox_XSize and self.BtnQ_HitBox_Y <= pos[1] \
                <= self.BtnQ_HitBox_YSize:

            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()
            MainWindow()  # Open MainWindow
            self.running = False

        # Swich form R-s
        elif 15 <= pos[0] <= 165 and 300 <= pos[1] <= 470:
            self.Form = "Rectangles"
        # Swich form R
        elif 175 <= pos[0] <= 325 and 300 <= pos[1] <= 470:
            self.Form = "Rectangle"
        # Swich form Circ
        elif 335 <= pos[0] <= 485 and 300 <= pos[1] <= 470:
            self.Form = "Circle"

        # Swich Color
        elif 15 <= pos[0] <= 165 and 510 <= pos[1] <= 610:
            self.Brick_Color = "Random"
        # Swich form R
        elif 175 <= pos[0] <= 325 and 510 <= pos[1] <= 610:
            self.Brick_Color = "Girls"
        # Swich form Circ
        elif 335 <= pos[0] <= 485 and 510 <= pos[1] <= 610:
            self.Brick_Color = "Forest"

        # Open Sett_file and replace "Theme"
        with open("settings.json") as file:
            data = json.load(file)
            data["Form"] = self.Form
            data["Colors"] = self.Brick_Color
            with open("settings.json", "w") as file:
                json.dump(data, file, indent=4)

        self.draw()

    # Draw on window: Title, other sett.
    def draw(self):
        # draw tittle "NickName"
        font = pygame.font.SysFont('arial', 24)
        text = font.render("NickName:", True, self.BgColor)
        text_x = (self.width // 2 - text.get_width() // 2) - 48
        text_y = 195
        self.screen.blit(text, (text_x, text_y))

        # draw NickName
        txt_surface = self.font.render(self.NickName, True, self.BgColor)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        # Blit the text.
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(self.screen, self.BgColor, self.input_box, 2)

        # draw title
        font = pygame.font.SysFont('arial', 40)
        text = font.render("GAME SETTINGS", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 40
        self.screen.blit(text, (text_x, text_y))

        # draw ChB "Music"
        # draw text
        font = pygame.font.SysFont('arial', 24)
        text = font.render("Music", True, self.BgColor)
        text_x = self.ChB_Music_posX
        text_y = self.ChB_Music_posY
        self.screen.blit(text, (text_x, text_y))

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.Music:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))
        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))

        # draw ChB "Sound"
        # draw text
        font = pygame.font.SysFont('arial', 24)
        text = font.render("Sounds", True, self.BgColor)
        text_x = self.ChB_Sound_posX
        text_y = self.ChB_Sound_posY
        self.screen.blit(text, (text_x, text_y))

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.Sound:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))
        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))

        # draw ChB "Theme"
        # draw text
        font = pygame.font.SysFont('arial', 22)
        text = font.render("Dark Theme", True, self.BgColor)
        text_x = self.ChB_Theme_posX
        text_y = self.ChB_Theme_posY
        self.screen.blit(text, (text_x, text_y))

        # draw ChB
        ChB_x = text_x - 25
        ChB_y = text_y - 2

        if self.DarkTheme:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x + 3, ChB_y + 3, 14, 14))

        else:
            pygame.draw.rect(self.screen, self.BgColor, (ChB_x, ChB_y, 20, 20))
            pygame.draw.rect(self.screen, self.TextColor, (ChB_x + 2, ChB_y + 2, 16, 16))
# Egor
        # Btn "Quit"
        font = pygame.font.SysFont('arial', 25)
        text = font.render("Quit", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 650
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 3)
        self.BtnQ_HitBox_X = text_x - 15
        self.BtnQ_HitBox_Y = text_y - 10
        self.BtnQ_HitBox_XSize = text_x + 235
        self.BtnQ_HitBox_YSize = text_y + 50

        # Theme of Bricks
        font = pygame.font.SysFont('arial', 24)
        text = font.render("Brick Form:", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 270
        self.screen.blit(text, (text_x, text_y))

        # Theme of Bricks
        font = pygame.font.SysFont('arial', 24)
        text = font.render("Brick Color:", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 480
        self.screen.blit(text, (text_x, text_y))

        self.colors = {'Random': {'light': ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30)),
                                  'dark': ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))},
                       'Girls': {'light': ((167, 0, 179), (157, 28, 166), (243, 82, 255), (183, 0, 255)),
                                 'dark': ((122, 3, 130), (70, 21, 74), (119, 30, 125), (85, 0, 255))},
                       'Forest': {'light': ((0, 168, 81), (15, 196, 2), (65, 184, 57), (58, 133, 77)),
                                  'dark': ((0, 105, 51), (10, 143, 0), (32, 115, 26), (8, 38, 15))}
                       }
        # Rectangles
        pygame.draw.rect(self.screen, self.BgColor, (15, 300, 150, 170), 2)
        pygame.draw.rect(self.screen, self.colors[self.Brick_Color]['dark'][3],
                         (55, 350, 70,
                          70), 0, 3)
        pygame.draw.rect(self.screen, self.colors[self.Brick_Color]['light'][3],
                         (55, 350, 66,
                          66), 0, 3)
        pygame.draw.circle(self.screen, self.colors[self.Brick_Color]['dark'][3],
                           (90,
                            385), 15.5)
        if self.Form == "Rectangles":
            pygame.draw.rect(self.screen, self.BgColor, (20, 305, 140, 15))
        # Rectangle
        pygame.draw.rect(self.screen, self.BgColor, (175, 300, 150, 170), 2)
        pygame.draw.rect(self.screen, self.colors[self.Brick_Color]['dark'][3],
                         (215, 350, 70,
                          70), 0)
        pygame.draw.rect(self.screen, self.colors[self.Brick_Color]['light'][3],
                         (215, 350, 66,
                          66), 0)
        pygame.draw.circle(self.screen, self.colors[self.Brick_Color]['dark'][3],
                           (250,
                            385), 15.5)
        if self.Form == "Rectangle":
            pygame.draw.rect(self.screen, self.BgColor, (180, 305, 140, 15))
        # Circle
        pygame.draw.rect(self.screen, self.BgColor, (335, 300, 150, 170), 2)
        pygame.draw.circle(self.screen, self.colors[self.Brick_Color]['dark'][3],
                           (410,
                            385), 30)
        pygame.draw.circle(self.screen, self.colors[self.Brick_Color]['light'][3],
                           (408,
                            382), 27)
        if self.Form == "Circle":
            pygame.draw.rect(self.screen, self.BgColor, (340, 305, 140, 15))

        # Random
        pygame.draw.rect(self.screen, self.BgColor, (15, 510, 150, 100), 2)
        if self.Brick_Color == "Random":
            pygame.draw.rect(self.screen, self.BgColor, (20, 515, 140, 15))
        pygame.draw.rect(self.screen, self.colors["Random"]["light"][0], (20, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Random"]["light"][1], (68, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Random"]["light"][2], (115, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Random"]["dark"][1], (20, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Random"]["light"][2], (68, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Random"]["dark"][3], (115, 575, 43, 30))

        # Girls Style
        pygame.draw.rect(self.screen, self.BgColor, (175, 510, 150, 100), 2)
        if self.Brick_Color == "Girls":
            pygame.draw.rect(self.screen, self.BgColor, (180, 515, 140, 15))
        pygame.draw.rect(self.screen, self.colors["Girls"]["light"][0], (180, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Girls"]["light"][1], (228, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Girls"]["light"][2], (275, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Girls"]["dark"][1], (180, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Girls"]["light"][2], (228, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Girls"]["dark"][3], (275, 575, 43, 30))

        # Forest
        pygame.draw.rect(self.screen, self.BgColor, (335, 510, 150, 100), 2)
        if self.Brick_Color == "Forest":
            pygame.draw.rect(self.screen, self.BgColor, (340, 515, 140, 15))
        pygame.draw.rect(self.screen, self.colors["Forest"]["light"][0], (340, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Forest"]["light"][1], (388, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Forest"]["light"][2], (435, 540, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Forest"]["dark"][1], (340, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Forest"]["light"][2], (388, 575, 43, 30))
        pygame.draw.rect(self.screen, self.colors["Forest"]["dark"][3], (435, 575, 43, 30))

        if pygame.mouse.get_focused():  # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)

        pygame.display.flip()

# Maxim
class Levels_Window:
    def __init__(self):
        global cursor
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        pygame.display.set_caption('Game')
        self.running = True
        self.error = False

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

        # Sounds
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')

        # Play Music
        if self.Music:
            pygame.mixer.music.unpause()

        # Staff
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Program
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
            self.screen.fill(self.TextColor)  # Fill display color
            self.draw()  # draw all

    def draw(self):
        self.all_sprites = pygame.sprite.Group()

        # Classic levels
        font = pygame.font.SysFont('arial', 40)
        text = font.render("CLASSIC", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 13
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.line(self.screen, self.BgColor, (0, 50), (500, 50), 4)

        sp1_l1 = pygame.sprite.Sprite()
        sp1_l1.image = pygame.image.load("Data/Sprites/logo_1level_unlock.png")
        sp1_l1.rect = sp1_l1.image.get_rect()
        sp1_l1.rect.x, sp1_l1.rect.y = 50, 70

        sp1_l2 = pygame.sprite.Sprite()
        sp1_l2.image = pygame.image.load("Data/Sprites/logo_2level_unlock.png")
        sp1_l2.rect = sp1_l2.image.get_rect()
        sp1_l2.rect.x, sp1_l2.rect.y = 200, 70

        sp1_l3 = pygame.sprite.Sprite()
        sp1_l3.image = pygame.image.load("Data/Sprites/logo_3level_lock.png")
        sp1_l3.rect = sp1_l3.image.get_rect()
        sp1_l3.rect.x, sp1_l3.rect.y = 350, 70


        #survival levels
        font = pygame.font.SysFont('arial', 40)
        text = font.render("SURVIVAL", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 233
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.line(self.screen, self.BgColor, (0, 270), (500, 270), 4)

        sp2_l1 = pygame.sprite.Sprite()
        sp2_l1.image = pygame.image.load("Data/Sprites/logo_1level_lock.png")
        sp2_l1.rect = sp2_l1.image.get_rect()
        sp2_l1.rect.x, sp2_l1.rect.y = 50, 290

        sp2_l2 = pygame.sprite.Sprite()
        sp2_l2.image = pygame.image.load("Data/Sprites/logo_2level_lock.png")
        sp2_l2.rect = sp2_l2.image.get_rect()
        sp2_l2.rect.x, sp2_l2.rect.y = 200, 290

        sp2_l3 = pygame.sprite.Sprite()
        sp2_l3.image = pygame.image.load("Data/Sprites/logo_3level_lock.png")
        sp2_l3.rect = sp2_l3.image.get_rect()
        sp2_l3.rect.x, sp2_l3.rect.y = 350, 290

        # puzzle levels
        font = pygame.font.SysFont('arial', 40)
        text = font.render("PUZZLE", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 453
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.line(self.screen, self.BgColor, (0, 490), (500, 490), 4)

        sp3_l1 = pygame.sprite.Sprite()
        sp3_l1.image = pygame.image.load("Data/Sprites/logo_1level_lock.png")
        sp3_l1.rect = sp3_l1.image.get_rect()
        sp3_l1.rect.x, sp3_l1.rect.y = 50, 510

        sp3_l2 = pygame.sprite.Sprite()
        sp3_l2.image = pygame.image.load("Data/Sprites/logo_2level_lock.png")
        sp3_l2.rect = sp3_l2.image.get_rect()
        sp3_l2.rect.x, sp3_l2.rect.y = 200, 510

        sp3_l3 = pygame.sprite.Sprite()
        sp3_l3.image = pygame.image.load("Data/Sprites/logo_3level_lock.png")
        sp3_l3.rect = sp3_l3.image.get_rect()
        sp3_l3.rect.x, sp3_l3.rect.y = 350, 510

        self.all_sprites.add(sp1_l1, sp1_l2, sp1_l3, sp2_l1, sp2_l2, sp2_l3, sp3_l1, sp3_l2, sp3_l3)

        # Btn "Quit"
        font = pygame.font.SysFont('arial', 25)
        text = font.render("Quit", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 650
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 3)
        self.BtnQ_HitBox_X = text_x - 15
        self.BtnQ_HitBox_Y = text_y - 10
        self.BtnQ_HitBox_XSize = text_x + 235
        self.BtnQ_HitBox_YSize = text_y + 50
        if pygame.mouse.get_focused():  # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)

        self.all_sprites.draw(self.screen)
        if pygame.mouse.get_focused():  # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()

    def click(self, pos):

        if not self.error:
            sp = list(self.all_sprites)
            for i in sp:
                x, y, x2, y2 = i.rect.x, i.rect.y, i.rect.x + i.rect.width, i.rect.y + i.rect.height
                if x - 10 <= pos[0] <= x2 and y - 10 <= pos[1] <= y2:
                    if sp.index(i) + 1 <= 2:
                        if sp.index(i) + 1 == 1:
                            self.running = False
                            if self.Sound:
                                pygame.mixer.music.pause()
                                self.sound_push_button.play()
                                if self.Music:
                                    pygame.mixer.music.unpause()
                            First_GM()
                        elif sp.index(i) + 1 == 2:
                            if self.Sound:
                                pygame.mixer.music.pause()
                                self.sound_push_button.play()
                                if self.Music:
                                    pygame.mixer.music.unpause()
                            self.running = False
                            Second_GM()

        else:
            self.error = False
            self.draw()

        # Close levels window
        if self.BtnQ_HitBox_X <= pos[0] <= self.BtnQ_HitBox_XSize and self.BtnQ_HitBox_Y <= pos[1] \
             <= self.BtnQ_HitBox_YSize:

            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()

            MainWindow()  # Open MainWindow
            self.running = False

# Egor
class Records:
    def __init__(self):
        global cursor
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        pygame.display.set_caption('Game')
        self.running = True

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

        if self.Music:
            pygame.mixer.music.unpause()
        self.sound_push_button = pygame.mixer.Sound('Data/Sounds/push_button.mp3')
        self.sound_push_keywords = pygame.mixer.Sound('Data/Sounds/push_keywords.mp3')


        # Staff
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
            self.screen.fill(self.TextColor)  # Fill display color
            self.draw()  # draw all

    def draw(self):
        font = pygame.font.Font(None, 30)
        text = font.render("PLAYER", True, self.BgColor)
        text_x = 30
        text_y = 13
        self.screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 30)
        text = font.render("TOTAL SCORE", True, self.BgColor)
        text_x = 320
        text_y = 13
        self.screen.blit(text, (text_x, text_y))

        n = 0
        records = read_records()

        for number, item in enumerate(records):
            font = pygame.font.Font('Data/Fonts/asymbols.ttf', 24)
            text = font.render(f'{number + 1}.', True, self.BgColor)
            text_x = 7
            text_y = 55 + n
            self.screen.blit(text, (text_x, text_y))

            font = pygame.font.Font('Data/Fonts/asymbols.ttf', 30)
            text = font.render(item[0], True, self.BgColor)
            text_x = 30
            text_y = 51 + n
            self.screen.blit(text, (text_x, text_y))

            font = pygame.font.Font('Data/Fonts/asymbols.ttf', 24)
            text = font.render(item[1], True, self.BgColor)
            text_x = 320
            text_y = 55 + n
            self.screen.blit(text, (text_x, text_y))

            n += 50

        font = pygame.font.SysFont('arial', 25)
        text = font.render("Quit", True, self.BgColor)
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 650
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, self.BgColor, (text_x - 10, text_y - 10,
                                                     text.get_width() + 20, text.get_height() + 20), 3)
        self.BtnQ_HitBox_X = text_x - 15
        self.BtnQ_HitBox_Y = text_y - 10
        self.BtnQ_HitBox_XSize = text_x + 235
        self.BtnQ_HitBox_YSize = text_y + 50

        if pygame.mouse.get_focused():  # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()

    def click(self, pos):
        # If sound On -> play sound
        if self.Sound:
            pygame.mixer.music.pause()
            self.sound_push_button.play()
            if self.Music:
                pygame.mixer.music.unpause()

        if self.BtnQ_HitBox_X <= pos[0] <= self.BtnQ_HitBox_XSize and self.BtnQ_HitBox_Y <= pos[1] \
                <= self.BtnQ_HitBox_YSize:

            if self.Sound:
                pygame.mixer.music.pause()
                self.sound_push_button.play()
                if self.Music:
                    pygame.mixer.music.unpause()
            MainWindow()  # Open MainWindow
            self.running = False


MainWindow()