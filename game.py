import pygame

from library.views import StartGame, Accounts, WinPopup, DefeatPopup, NewAccount, Levels
from library.levels import Level1, Level2, Level3
from library.db import db
from library.Controller import Controller

db.init()

# CONFIG
WIDTH = 800
HEIGHT = 600
FPS = 60
CAPTION = "Mad Snake"
WHITE = (255, 255, 255)

# pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

icon = pygame.image.load('assets/favicon.png')
pygame.display.set_icon(icon)

running = True
clock = pygame.time.Clock()

controller = Controller(startView='start', config={
    'WIDTH': WIDTH,
    'HEIGHT': HEIGHT,
    'SCORE_TARGET': 2
})

controller.setViews([
    StartGame('start', controller),
    Accounts('users', controller),
    NewAccount('newUser', controller),
    Levels('levels', controller),
    Level1('level1', 1, controller),
    Level2('level2', 2, controller),
    Level3('level3', 3, controller),
])

controller.setPopups([
    WinPopup('win', controller),
    DefeatPopup('defeat', controller),
])

# CYCLE
while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        controller.events(event)

    # Update
    controller.update()

    # Render
    screen.fill(WHITE)

    controller.render(screen)

    pygame.display.flip()
    clock.tick(FPS)


db.close()
# figma.getNodeById(figma.activeUsers[0].selection).children.map(x => `pygame.Rect(${x.x}, ${x.y}, ${x.width}, ${x.height}),`).join('\n')