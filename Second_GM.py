import pygame
import json
from random import choice, randint
import time

pygame.init()
pygame.mixer.init()


class Board:  # General class for game modes
    def __init__(self, screen, width, height):
        self.fig_w, self.fig_h = 5, 5
        self.empty = 'o'
        self.figures = {'S': [['ooooo',
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
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
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
        self.side_freq, self.down_freq = 0.15, 0.1  # Movement to the side and down
        self.side_margin = 10
        self.top_margin = self.height_w - (self.height * self.cell_size) - 5
        self.clock = pygame.time.Clock()
        self.last_move_down = time.time()
        self.last_side_move = time.time()
        self.last_fall = time.time()
        self.going_down = False  # Is it possible to move to the down
        self.going_left = False  # Is it possible to move to the left
        self.going_right = False  # Is it possible to move to the right
        self.level, self.fall_speed = self.calcSpeed()
        self.fallingFig = self.getNewFig()
        self.nextFig = self.getNewFig()
        while running:
            if self.fallingFig is None:  # If there are no falling shapes, we generate a new one
                self.fallingFig = self.nextFig
                self.nextFig = self.getNewFig()
                self.last_fall = time.time()

                if not self.checkPos(self.fallingFig):
                    exit()  # If there is no free space on the playing field - the game is over, final window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.going_left = False
                    if event.key == pygame.K_RIGHT:
                        self.going_right = False
                    if event.key == pygame.K_DOWN:
                        self.going_down = False

                if event.type == pygame.KEYDOWN:  # Moving the figure to the right and left
                    if event.key == pygame.K_LEFT and self.checkPos(self.fallingFig, adjX=-1):
                        self.fallingFig['x'] -= 1
                        self.going_left = True
                        self.going_right = False
                        self.last_side_move = time.time()

                    if event.key == pygame.K_RIGHT and self.checkPos(self.fallingFig, adjX=1):
                        self.fallingFig['x'] += 1
                        self.going_right = True
                        self.going_left = False
                        self.last_side_move = time.time()

                    if event.key == pygame.K_UP and self.score < 21000:  # Rotate the figure if there is room
                        self.fallingFig['rotation'] = (self.fallingFig['rotation'] + 1) \
                                                      % len(self.figures[self.fallingFig['shape']])
                        if not self.checkPos(self.fallingFig):
                            self.fallingFig['rotation'] = (self.fallingFig['rotation'] - 1) \
                                                          % len(self.figures[self.fallingFig['shape']])

                    if event.key == pygame.K_DOWN:  # Speed up the fall of the figure
                        self.going_down = True
                        if self.checkPos(self.fallingFig, adjY=1):
                            self.fallingFig['y'] += 1
                        self.last_move_down = time.time()

            # Controlling the fall of the figure while holding down the keys
            if (self.going_left or self.going_right) and time.time() - self.last_side_move > self.side_freq:
                if self.going_left and self.checkPos(self.fallingFig, adjX=-1):
                    self.fallingFig['x'] -= 1
                elif self.going_right and self.checkPos(self.fallingFig, adjX=1):
                    self.fallingFig['x'] += 1
                self.last_side_move = time.time()

            if self.going_down and time.time() - self.last_move_down > self.down_freq \
                    and self.checkPos(self.fallingFig, adjY=1):
                self.fallingFig['y'] += 1
                self.last_move_down = time.time()

            if time.time() - self.last_fall > self.fall_speed:  # Free fall of the figure
                if not self.checkPos(self.fallingFig, adjY=1):
                    self.addBoard(self.fallingFig)  # The figure has landed, add it to the contents of the board
                    self.score += self.clearCompleted() * 300
                    self.level, self.fall_speed = self.calcSpeed()
                    self.fallingFig = None
                else:  # The figure hasn't landed yet, we keep moving down
                    self.fallingFig['y'] += 1
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

    def clearCompleted(self): # Removing filled rows and shifting the top rows down
        removed_lines = 0
        y = self.height - 1
        while y >= 0:
            if self.isCompleted(y):
                for pushDownY in range(y, 0, -1):
                    for x in range(self.width):
                        self.board[x][pushDownY] = self.board[x][pushDownY - 1]
                for x in range(self.width):
                    self.board[x][0] = self.empty
                removed_lines += 1
            else:
                y -= 1
        return removed_lines

    def incup(self, x, y):
        return self.width > x >= 0 and y < self.height

    def checkPos(self, fig, adjX=0, adjY=0): # Checks if the shape is within the board boundaries without colliding with other shapes
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                above_board = y + fig['y'] + adjY < 0
                if above_board or self.figures[fig['shape']][fig['rotation']][y][x] == self.empty:
                    continue
                if not self.incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                    return False
                if self.board[x + fig['x'] + adjX][y + fig['y'] + adjY] != self.empty:
                    return False
        return True

    def addBoard(self, fig):
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                if self.figures[fig['shape']][fig['rotation']][y][x] != self.empty:
                    self.board[x + fig['x']][y + fig['y']] = fig['color']

    def calcSpeed(self):
        level = int(0 / 10) + 1
        fall_speed = 0.27 - (level * 0.02)
        return level, fall_speed

    def getNewFig(self): # Returns a new shape with a random color and rotation angle
        shape = choice(list(self.figures.keys()))
        newFigure = {'shape': shape,
                     'rotation': randint(0, len(self.figures[shape]) - 1),
                     'x': int(self.width / 2) - int(self.fig_w / 2),
                     'y': -2,
                     'color': randint(0, len(self.colors) - 1)}
        return newFigure

    def convertCoords(self, block_x, block_y):
        return (self.side_margin + (block_x * self.cell_size)), \
            (self.top_margin + (block_y * self.cell_size))

    def drawBlock(self, block_x, block_y, color, pixelx=None, pixely=None): # Drawing the square blocks that make up the figures
        if color == self.empty:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convertCoords(block_x, block_y)
        pygame.draw.rect(self.screen, self.colors[color],
                         (pixelx + 1, pixely + 1, self.cell_size - 1,
                          self.cell_size - 1),
                         0, 3)
        pygame.draw.rect(self.screen, self.lightcolors[color],
                         (pixelx + 1, pixely + 1, self.cell_size - 4,
                          self.cell_size - 4), 0, 3)
        pygame.draw.circle(self.screen, self.colors[color],
                           (pixelx + self.cell_size / 2,
                            pixely + self.cell_size / 2), 5)

    def drawnextFig(self, fig):  # Preview of the next figure
        self.drawFig(fig, pixelx=self.width_w - 160, pixely=100)

    def drawFig(self, fig, pixelx=None, pixely=None):
        figToDraw = self.figures[fig['shape']][fig['rotation']]
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convertCoords(fig['x'], fig['y'])
        # Drawing figure elements
        for x in range(self.fig_w):
            for y in range(self.fig_h):
                if figToDraw[y][x] != self.empty:
                    self.drawBlock(None, None, fig['color'], pixelx + (x * self.cell_size),
                                   pixely + (y * self.cell_size))

    def render(self):
        if self.theme:
            themeColor = pygame.Color('white')
        else:
            themeColor = pygame.Color('black')
        pygame.draw.rect(self.screen, themeColor,
                         (self.side_margin - 4, self.top_margin - 4, (self.width * self.cell_size) + 8,
                         (self.height * self.cell_size) + 8), 5) # Border of the playing field
        for x in range(self.width):
            for y in range(self.height):
                self.drawBlock(x, y, self.board[x][y])
        self.drawnextFig(self.nextFig)
        if self.fallingFig is not None:
            self.drawFig(self.fallingFig)

        pygame.display.flip()


class Second_GM(Board):
    def __init__(self):
        self.size = self.width_w, self.height_w = 600, 750  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        Board.__init__(self, self.screen, 15, 31)

    def calcSpeed(self):
        score = self.score if self.score < 15000 else 15000
        level = int((score / 250) / 10) + 1
        fall_speed = 0.27 - (level * 0.03)
        return level, fall_speed


Second_GM()