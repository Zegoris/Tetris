import pygame
import json
from random import choice, randint
import time

pygame.init()
pygame.mixer.init()


class Board:  # General class for game modes
    def __init__(self, screen, width, height):
        self.tetraminesW, self.tetraminesH = 5, 5
        self.empty = 'o'
        self.tetramines = {'S': [['ooooo',
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
        running = True
        self.colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))
        self.lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
        self.width = width
        self.height = height
        self.board = [[self.empty] * height for _ in range(width)]  # Matrix of values of painted cells
        self.left = 0
        self.top = 0
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
        if self.theme:
            screen.fill(self.darkTheme)
        else:
            screen.fill(self.lightTheme)
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
        while running:
            if self.fallingTetramine is None:  # If there are no falling shapes, we generate a new one
                self.fallingTetramine = self.nextTetramine
                self.nextTetramine = self.newTetramine()
                self.last_fall = time.time()

                if not self.check(self.fallingTetramine):
                    exit()  # If there is no free space on the playing field - the game is over, FINAL WINDOW
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.left = False
                    if event.key == pygame.K_RIGHT:
                        self.right = False
                    if event.key == pygame.K_DOWN:
                        self.down = False

                if event.type == pygame.KEYDOWN:  # Moving the figure to the right and left
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

                    if event.key == pygame.K_UP and self.score < 21000:  # Rotate the figure if there is room
                        self.fallingTetramine['rotation'] = (self.fallingTetramine['rotation'] + 1) \
                                                            % len(self.tetramines[self.fallingTetramine['shape']])
                        if not self.check(self.fallingTetramine):
                            self.fallingTetramine['rotation'] = (self.fallingTetramine['rotation'] - 1) \
                                                                % len(self.tetramines[self.fallingTetramine['shape']])

                    if event.key == pygame.K_DOWN:  # Speed up the fall of the figure
                        self.down = True
                        if self.check(self.fallingTetramine, y0=1):
                            self.fallingTetramine['y'] += 1
                        self.last_down = time.time()

            # Controlling the fall of the figure while holding down the keys
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

            if time.time() - self.last_fall > self.fall_speed:  # Free fall of the figure
                if not self.check(self.fallingTetramine, y0=1):
                    self.addBoard(self.fallingTetramine)  # The figure has landed, add it to the contents of the board
                    self.score += self.clearCompleted() * 300
                    self.level, self.fall_speed = self.static()
                    self.fallingTetramine = None
                else:  # The figure hasn't landed yet, we keep moving down
                    self.fallingTetramine['y'] += 1
                    self.last_fall = time.time()
            if self.theme:
                self.screen.fill(self.darkTheme)
            else:
                self.screen.fill(self.lightTheme)
            self.render()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def isCompleted(self, y): # Check the presence of fully filled rows
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

    def check(self, fig, x0=0, y0=0): # Checks if the shape is within the board boundaries without colliding with other shapes
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                above_board = y + fig['y'] + y0 < 0
                if above_board or self.tetramines[fig['shape']][fig['rotation']][y][x] == self.empty:
                    continue
                if not self.inBoard(x + fig['x'] + x0, y + fig['y'] + y0):
                    return False
                if self.board[x + fig['x'] + x0][y + fig['y'] + y0] != self.empty:
                    return False
        return True

    def inBoard(self, x, y):
        return self.width > x >= 0 and y < self.height

    def addBoard(self, fig):
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if self.tetramines[fig['shape']][fig['rotation']][y][x] != self.empty:
                    self.board[x + fig['x']][y + fig['y']] = fig['color']

    def static(self):
        level = int(0 / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    def coords(self, x, y):
        return (self.side_fields + (x * self.cell_size)), \
            (self.upper_field + (y * self.cell_size))

    def newTetramine(self): # Returns a new shape with a random color and rotation angle
        shape = choice(list(self.tetramines.keys()))
        newTetramine = {'shape': shape,
                     'rotation': randint(0, len(self.tetramines[shape]) - 1),
                     'x': int(self.width / 2) - int(self.tetraminesW / 2),
                     'y': -2,
                     'color': randint(0, len(self.colors) - 1)}
        return newTetramine

    def drawBlock(self, block_x, block_y, color, x=None, y=None): # Drawing the square blocks that make up the figures
        if color == self.empty:
            return
        if x is None and y is None:
            x, y = self.coords(block_x, block_y)
        pygame.draw.rect(self.screen, self.colors[color],
                         (x + 1, y + 1, self.cell_size - 1,
                          self.cell_size - 1),
                         0, 3)
        pygame.draw.rect(self.screen, self.lightcolors[color],
                         (x + 1, y + 1, self.cell_size - 4,
                          self.cell_size - 4), 0, 3)
        pygame.draw.circle(self.screen, self.colors[color],
                           (x + self.cell_size / 2,
                            y + self.cell_size / 2), 5)

    def drawnextTetramine(self, tetramine):  # Preview of the next figure
        self.drawTetramine(tetramine, x0=self.widthW - 160, y0=100)

    def drawTetramine(self, fig, x0=None, y0=None):
        figToDraw = self.tetramines[fig['shape']][fig['rotation']]
        if x0 is None and y0 is None:
            x0, y0 = self.coords(fig['x'], fig['y'])
        # Drawing figure elements
        for x in range(self.tetraminesW):
            for y in range(self.tetraminesH):
                if figToDraw[y][x] != self.empty:
                    self.drawBlock(None, None, fig['color'], x0 + (x * self.cell_size),
                                   y0 + (y * self.cell_size))

    def render(self):
        if self.theme:
            themeColor = pygame.Color('white')
        else:
            themeColor = pygame.Color('black')
        pygame.draw.rect(self.screen, themeColor,
                         (self.side_fields - 4, self.upper_field - 4, (self.width * self.cell_size) + 8,
                          (self.height * self.cell_size) + 8), 5) # Border of the playing field
        for x in range(self.width):
            for y in range(self.height):
                self.drawBlock(x, y, self.board[x][y]) # Already landed figures
        self.drawnextTetramine(self.nextTetramine) # Preview of the next figure
        if self.fallingTetramine is not None:
            self.drawTetramine(self.fallingTetramine)  # Drawing a falling figure

        pygame.display.flip()


class Second_GM(Board):
    def __init__(self):
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        Board.__init__(self, self.screen, 15, 31)

    def static(self):
        score = self.score if self.score < 15000 else 15000
        level = int((score / 250) / 10) + 1
        fall_speed = 0.27 - (level * 0.03)
        return level, fall_speed


Second_GM()