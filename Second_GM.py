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


def write_records(user, gm, score):
    yes = False
    with open('records.csv', encoding="utf8") as csvf:
        reader = csv.reader(csvf, delimiter=',', quotechar='"')
        reader = list(reader)
    os.remove('records.csv')
    for i in reader:
        if user in i:
            yes = True
            index = reader.index(i)
            if gm == 1:
                if score > int(reader[index][1]):
                    reader[index] = [user, score, i[2]]

            elif gm == 2:
                if score > int(reader[index][2]):
                    reader[index] = [user, i[1], score]
            break
    if not yes:
        if gm == 1:
            reader.append([user, score, '0'])

        elif gm == 2:
            reader.append([user, '0', score])
    with open('records.csv', 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerows(reader)


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


class Board:  # General class for game modes
    def __init__(self, screen, width, height, game_mode):
        global cursor
        pygame.display.set_caption('Game')
        self.tetraminesW, self.tetraminesH = 5, 5
        self.empty = 'o'
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
        self.colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
        self.light_colors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
        self.width = width
        self.height = height
        self.board = [[self.empty] * height for _ in range(width)]  # Matrix of values of painted cells
        self.cell_size = 24
        self.score = 0
        self.screen = screen
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
        self.fps = 60
        self.side_frequency, self.down_frequency = 0.15, 0.1  # Movement to the side and down
        self.side_fields = 10
        self.upper_field = self.heightW - (self.height * self.cell_size) - 5
        self.clock = pygame.time.Clock()
        self.last_down = time.time()
        self.last_side = time.time()
        self.last_fall = time.time()
        self.down = False  # Is it possible to move to the down
        self.left = False  # Is it possible to move to the left
        self.right = False  # Is it possible to move to the right
        self.level, self.fall_speed = self.static()
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
                    Game_Over(self.score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.click(event.pos):
                        write_records(self.user, self.gm, self.score)
                        self.running = False
                        Game_Over(self.score)

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
            if (self.left or self.right) and time.time() - self.last_side > self.side_frequency:
                if self.left and self.check(self.fallingTetramine, x0=-1):
                    self.fallingTetramine['x'] -= 1

                elif self.right and self.check(self.fallingTetramine, x0=1):
                    self.fallingTetramine['x'] += 1
                self.last_side = time.time()

            if self.down and time.time() - self.last_down > self.down_frequency \
                    and self.check(self.fallingTetramine, y0=1):
                self.fallingTetramine['y'] += 1
                self.last_down = time.time()

            if time.time() - self.last_fall > self.fall_speed:  # Free fall of the tetramine
                if not self.check(self.fallingTetramine, y0=1):
                    self.add(self.fallingTetramine)  # The tetramine has landed, add it to the contents of the board
                    self.score += self.clearCompleted() * 300 if self.score <= 99999 else 99999
                    self.level, self.fall_speed = self.static()
                    self.fallingTetramine = None
                else:  # The tetramine hasn't landed yet, we keep moving down
                    self.fallingTetramine['y'] += 1
                    self.last_fall = time.time()
            self.screen.fill(self.themeColor)
            self.render()
            self.clock.tick(self.fps)

    def isCompleted(self, y):  # Check the presence of fully filled rows
        for x in range(self.width):
            if self.board[x][y] == self.empty:
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
                    self.board[x][0] = self.empty
                removed_lines += 1
            else:
                y0 -= 1
        return removed_lines

    def click(self, pos):
        # If Mouse Pos in HitBox True
        if self.button_HitBox_x - 10 <= pos[0] <= self.button_HitBox_sizeX\
                and self.button_HitBox_y - 12 <= pos[1] <= self.button_HitBox_sizeY:
            return True
        return False

    def check(self, tetramine, x0=0, y0=0):  # Checks if the tetramine is within the board boundaries without colliding with other tetramines
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                above_board = y + tetramine['y'] + y0 < 0
                if above_board or self.tetramines[tetramine['shape']][tetramine['rotation']][y][x] == self.empty:
                    continue

                if not self.inBoard(x + tetramine['x'] + x0, y + tetramine['y'] + y0):
                    return False

                if self.board[x + tetramine['x'] + x0][y + tetramine['y'] + y0] != self.empty:
                    return False
        return True

    def inBoard(self, x, y):
        return self.width > x >= 0 and y < self.height

    def add(self, tetramine):
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if self.tetramines[tetramine['shape']][tetramine['rotation']][y][x] != self.empty:
                    self.board[x + tetramine['x']][y + tetramine['y']] = tetramine['color']

    def static(self): # Calculating game's speed
        level = int(0 / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    def coords(self, x, y):
        return (self.side_fields + (x * self.cell_size)), \
            (self.upper_field + (y * self.cell_size))

    def newTetramine(self):  # Returns a new tetramine with a random color and rotation angle
        shape = choice(list(self.tetramines.keys()))
        newTetramine = {'shape': shape,
                        'rotation': randint(0, len(self.tetramines[shape]) - 1),
                        'x': int(self.width / 2) - int(self.tetraminesW / 2),
                        'y': -2,
                        'color': randint(0, len(self.colors) - 1)}
        return newTetramine

    def drawBlock(self, block_x, block_y, color, size, x=None, y=None):  # Drawing the square blocks that make up the tetramines
        if color == self.empty:
            return

        if x is None and y is None:
            x, y = self.coords(block_x, block_y)
        pygame.draw.rect(self.screen, self.colors[color],
                         (x + 1, y + 1, size - 1,
                          size - 1),
                         0, 3)
        pygame.draw.rect(self.screen, self.light_colors[color],
                         (x + 1, y + 1, size - 4,
                          size - 4), 0, 3)
        pygame.draw.circle(self.screen, self.colors[color],
                           (x + size / 2,
                            y + size / 2), 5)

    def drawnextTetramine(self, tetramine):  # Preview of the next tetramine
        self.drawTetramine(tetramine, self.cell_size + 10, x0=self.widthW - 200, y0=70)

    def drawTetramine(self, tetramine, size, x0=None, y0=None):
        tetramineDraw = self.tetramines[tetramine['shape']][tetramine['rotation']]
        if x0 is None and y0 is None:
            x0, y0 = self.coords(tetramine['x'], tetramine['y'])
        # Drawing tetramine elements
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if tetramineDraw[y][x] != self.empty:
                    self.drawBlock(None, None, tetramine['color'], size, x0 + (x * size),
                                   y0 + (y * size))

    def info(self): # Drawing information about user and score
        if self.theme:
            fontColor = pygame.Color('white')
        else:
            fontColor = pygame.Color((30, 61, 89))
        font_score = pygame.font.SysFont('symbol', 45)
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
        pygame.draw.rect(self.screen, borderColor,
                         (self.side_fields - 4, self.upper_field - 4, (self.width * self.cell_size) + 8,
                          (self.height * self.cell_size) + 8), 5)  # Border of the playing field

        for x in range(self.width):
            for y in range(self.height):
                self.drawBlock(x, y, self.board[x][y], size=self.cell_size)  # Already landed tetramine
        self.drawnextTetramine(self.nextTetramine)  # Preview of the next tetramine

        if self.fallingTetramine is not None:
            self.drawTetramine(self.fallingTetramine, size=self.cell_size)  # Drawing a falling tetramine

        if pygame.mouse.get_focused(): # Drawing a cursor
            cursor.rect.x, cursor.rect.y = pygame.mouse.get_pos()
            cursor_group.draw(self.screen)
        pygame.display.flip()


class Second_GM(Board): # Class of the second game mode
    def __init__(self):
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        Board.__init__(self, self.screen, 15, 31, game_mode=2)

    def static(self): # Calculating game's speed
        score = self.score if self.score < 15000 else 15000
        level = int((score / 250) / 10) + 1
        fall_speed = 0.27 - (level * 0.03)
        return level, fall_speed


Second_GM()