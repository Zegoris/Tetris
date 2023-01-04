import pygame

pygame.init()
coords = []
st1 = open('data/', encoding='utf8')
a = 0
b, c = 0, 0
st2 = st1.readlines()
for _ in st2:
    a = _
for i in range(len(a)):
    if a[i] == '(':
        b = i
    if a[i] == ')':
        c = i
        line = a[b + 1: c].split(';')
        if ',' in line[0]:
            line[0] = line[0].replace(',', '.')
        if ',' in line[1]:
            line[1] = line[1].replace(',', '.')
        coords.append([(float(line[0])), (float(line[1]))])
        b, c = 0, 0
size = width, height = 501, 501
screen = pygame.display.set_mode(size)
white = pygame.Color('white')
black = pygame.Color('black')
k = 1
coords1 = []
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
            k *= 2
        if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
            k /= 2
    for i in coords:
        x, y = i[1], i[0]
        coords1.append([float(x * k + 250.5), float(y * k + 250.5)])
    screen.fill(black)
    pygame.draw.polygon(screen, white, coords1, 1)
    coords1 = []
    pygame.display.flip()