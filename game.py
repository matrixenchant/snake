import pygame

from library.views import StartGame, Accounts, WinPopup, DefeatPopup, NewAccount, Levels, Level1
from library.db import db
from library.Controller import Controller

db.init()

# CONFIG
WIDTH = 800
HEIGHT = 600
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
    'FPS': 160,
    'SCORE_TARGET': 2
})

controller.setViews([
    StartGame('start', controller),
    Accounts('users', controller),
    NewAccount('newUser', controller),
    Levels('levels', controller),
    Level1('level1', controller),
])

controller.setPopups({
    'win': WinPopup(controller),
    'defeat': DefeatPopup(controller)
})


#                            active_view relations

#   1         2          3          4         5         6           7         8
# intro   accounts  add_account   levels   level1     level2     level3     level4

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
    clock.tick(controller.fps)


db.close()