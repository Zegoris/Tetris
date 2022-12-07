import pygame
import json
from random import choice
pygame.init()
pygame.mixer.init()


class Board: # General class for game modes
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)] # Matrix of values of painted cells
        self.left = 0
        self.top = 0
        self.cell_size = 40
        self.screen = screen
        self.lightTheme = (245, 240, 225)
        self.darkTheme = (30, 61, 89)
        with open("settings.json") as file:
            data = json.load(file)
            self.music = data["Music"]
            self.sounds = data["Sounds"]
            self.theme = data['DarkTheme']
            self.lightTheme = tuple(data['Color']['Light'])
            self.darkTheme = tuple(data['Color']['Dark'])
        if self.theme:
            screen.fill(self.darkTheme)
        else:
            screen.fill(self.lightTheme)

    def cell(self, x, y): # Getting the coordinate of the cell in the matrix
        if self.width * self.cell_size + self.left >= x >= self.left \
                and self.height * self.cell_size + self.top >= y >= self.top:
            row, col = abs((x - self.left) // self.cell_size), \
                       abs((y - self.top) // self.cell_size)
            self.negative(row, col)

    def negative(self, row, col): # Painting the cell
        color = choice([1, 2, 3, 4, 5]) # Selecting the color of the object
        object = choice([[(-2, 0), (-1, 0), (0, 0), (1, 0)], # Selecting the form of the object
                         [(-1, 0), (0, 0), (1, 0), (0, 1)],
                         [(-1, 0), (0, 0), (0, 1), (-1, 1)],
                         [(-1, 0), (0, 0), (1, 0), (1, 1)],
                         [(0, 0), (1, 0), (0, 1), (-1, 1)]])
        for i in object:
            self.board[col + i[0]][row + i[1]] = color
        print(self.board)

    def render(self):
        if self.theme:
            themeColor = pygame.Color('white')
        else:
            themeColor = pygame.Color('black')
        for col in range(self.height):
            for row in range(self.width):
                if self.board[col][row] == 0:
                    pygame.draw.rect(self.screen, themeColor,
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 2)
                elif self.board[col][row] == 1:
                    pygame.draw.rect(self.screen, pygame.Color((255, 0, 127)),
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 0)
                elif self.board[col][row] == 2:
                    pygame.draw.rect(self.screen, pygame.Color((0, 204, 204)),
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 0)
                elif self.board[col][row] == 3:
                    pygame.draw.rect(self.screen, pygame.Color((255, 128, 0)),
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 0)
                elif self.board[col][row] == 4:
                    pygame.draw.rect(self.screen, pygame.Color((0, 102, 0)),
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 0)
                elif self.board[col][row] == 5:
                    pygame.draw.rect(self.screen, pygame.Color((76, 0, 153)),
                                     (row * self.cell_size + self.left,
                                      col * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size), 0)


class First_GM(Board): # Class of the first game mode
    def __init__(self):
        self.size = self.width, self.height = 500, 700  # Window Size
        self.screen = pygame.display.set_mode(self.size)  # Screen Setting
        running = True
        Board.__init__(self, self.screen, 12, 18)
        self.render()  # draw board
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Stop Programm
                    running = False


First_GM()
