import pygame
import random
import time
from utils import get_image, checkInSnake, InputBox
from random import randint
from Snake import Snake
import views
import db

db.init()

# CONFIG
WIDTH = 800
HEIGHT = 600
CAPTION = "Mad Snake"
WHITE = (255, 255, 255)

# GAME SETTINGS
FPS = 160
TARGET_SCORE = 2

STAGES = [
    {
        'name': 'EASY',
        'colors': [(47, 131, 50),(31, 97, 34)]
    },
    {
        'name': 'NORMAL',
        'colors': [(221, 214, 53),(200, 194, 43)]
    },
    {
        'name': 'HARD',
        'colors': [(242, 186, 40),(222, 170, 37)]
    },
    {
        'name': 'VERY_HARD',
        'colors': [(218, 73, 42),(195, 62, 33)]
    },
    {
        'name': 'INSANE',
        'colors': [(219, 25, 25),(188, 20, 20)]
    },
    {
        'name': 'IMPOSSIBLE',
        'colors': [(0, 0, 0),(0, 0, 0)]
    },
]
ACTIVE_STAGE = 0

# pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

icon = pygame.image.load('favicon.png')
pygame.display.set_icon(icon)

running = True
game = False
status = 'playing'
# 'playing' | 'defeat' | 'win'
clock = pygame.time.Clock()
score = 0
active_view = 1
active_level = 0
is_food_spawn = False
enable_gui = False
is_paused = False

# RESOURCES
main_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 13)
stage_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 15)

food_variants = [
    ['assets/food.png', 1],
    ['assets/food2.png', 3]
]
class Food(pygame.sprite.Sprite):
    def __init__(self, snake, group):
        pygame.sprite.Sprite.__init__(self)
        variant = food_variants[randint(0,1)]
        self.snake = snake
        self.width = 20
        self.height = 25
        self.image = pygame.image.load(variant[0])
        self.rect = self.image.get_rect()
        self.weight = variant[1]
        self.add(group)
        self.spawnTime = int(time.time())
        self.spawn()
        self.is_update = True

    def spawn(self):
        x = random.randint(self.width+10, WIDTH-self.width-10)
        y = random.randint(50, HEIGHT-self.height-10)
        while checkInSnake(self.snake.parts, 15, x): x = random.randint(10, WIDTH-10)
        while checkInSnake(self.snake.parts, 15, y): y = random.randint(50, HEIGHT-10)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(x = x, y = y)

    def update(self):
        if not self.is_update: return
        if int(time.time()) - self.spawnTime > 5:
            self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Create snake
snake = Snake(WIDTH/2, HEIGHT-200)
snake.color_head = STAGES[ACTIVE_STAGE]['colors'][1]
snake.color_body = STAGES[ACTIVE_STAGE]['colors'][0]

# Create food
foods = pygame.sprite.Group()
food = Food(snake, foods)
# Spawn extra food
pygame.time.set_timer(pygame.USEREVENT, 8000)

def gameRestart():
    global score, ACTIVE_STAGE, status, FPS, snake, food, game, is_food_spawn, enable_gui
    score = 0
    ACTIVE_STAGE = 0
    status = 'playing'
    FPS = 160
    snake.restart()
    food = False
    game = True
    is_food_spawn = True
    enable_gui = True

def gamePause():
    global is_food_spawn
    is_food_spawn = False
    for el in foods:
        el.is_update = False
    snake.stop()

def gameUnpause():
    global is_food_spawn
    is_food_spawn = True
    for el in foods:
        el.is_update = True
    snake.resume()

# Views
#field = InputBox(200, 200, 200, 30, main_font)
intro = views.startGame(1)
accounts = views.Accounts(2)
new_acc = views.NewAccount(3)
levels = views.Levels(4)

level1 = views.Level1(5)
level2 = views.Level2(6)
level3 = views.Level3(7, snake)
views_group = [intro, accounts, new_acc, levels, level1, level2, level3]
levels_group = [level1, level2, level3]

#                            active_view relations

#   1         2          3          4         5         6           7         8
# intro   accounts  add_account   levels   level1     level2     level3     level4


def addLvl():
    max_lvl = views.USER['max_lvl']
    if active_level == max_lvl:
        views.updateLvlUser(max_lvl+1)
        user_id = views.USER['id']
        db.update_user(user_id, views.USER['max_lvl'])

# CYCLE
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if is_paused:
                gameUnpause()
                is_paused = False
            else:
                gamePause()
                is_paused = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and status != 'playing':
            if status == 'win': addLvl()
            gameRestart()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m and status != 'playing':
            if status == 'win': addLvl()

            active_view = 4
            active_level = 0
            enable_gui = False
            snake.hide()
            status = 'playing'
        if event.type == pygame.USEREVENT and is_food_spawn:
            Food(snake, foods)

        snake.events(event)
        if intro.handle_event(event): active_view = 2
        changer = accounts.handle_event(event)
        if changer: active_view = changer
        if new_acc.handle_event(event): active_view = 4

        level = levels.handle_event(event)
        if level:
            active_level = level - 4
            active_view = level
            gameRestart()

    # Update
    for view in views_group:
        view.update(active_view)


    if status == 'defeat':
        # Game over
        game = False
        snake.stop()
        snake.color_head = (255, 0, 0)
    elif game:
        game = True
        status = 'playing'
        foods.update()
        snake.update()

        if snake.isCollide:
            status = 'defeat'

        # Check collide with level obstacles
        if active_level != 0:
            obsRects = levels_group[active_level-1].obsRects
            obsCollide = pygame.Rect.collidelist(snake.get_rect(), obsRects)
            if obsCollide != -1:
                snake.isCollide = True

        # Check collide snake with food
        foodCollide = pygame.Rect.collidelist(snake.get_rect(), [x.get_rect() for x in foods.sprites()])
        if foodCollide != -1:
            sprite = foods.sprites()[foodCollide]
            snake.grow()
            score += sprite.weight
            foods.remove(sprite)
            Food(snake, foods)

        # Change STAGES
        if score != 0 and score >= (ACTIVE_STAGE+1) * TARGET_SCORE:
            # WIN
            if ACTIVE_STAGE == len(STAGES)-1:
                game = False
                snake.stop()
                status = 'win'
            # NEXT STAGES
            else:
                ACTIVE_STAGE += 1
                FPS += 20
                if ACTIVE_STAGE == len(STAGES)-1:
                    snake.enableRainbow()
                else:
                    snake.color_head = STAGES[ACTIVE_STAGE]['colors'][1]
                    snake.color_body = STAGES[ACTIVE_STAGE]['colors'][0]
            
    # Render
    screen.fill(WHITE)

    # Views
    for view in views_group:
        view.draw(screen)

    if game:
        foods.draw(screen)
    snake.render(screen)

    # Levels obstacles
    for lvl in levels_group:
        lvl.drawObs(screen)

    # GUI
    if enable_gui:
        views.gui(screen, stage_font, main_font, score, STAGES[ACTIVE_STAGE]['name'], STAGES[ACTIVE_STAGE]['colors'][1])
    
    # Statuses
    if status == 'defeat':
        screen.blit(get_image('assets/game_over.png'), (215, 206))
    if status == 'win':
        screen.blit(get_image('assets/win.png'), (111, 117))

    pygame.display.flip()
    clock.tick(FPS)


db.close()