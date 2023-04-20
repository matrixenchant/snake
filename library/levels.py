import pygame
from random import randint
from .views import View
from .utils import get_image, AnimatedObject, ProjectileEmitter, Object, Enemy, Aster

from .Snake import Snake
from .Food import Food

class Level(View):
    def __init__(self, slug, level, controller):
        super().__init__(slug, controller)

        self.level = level
        self.score = 0

        self.isPause = False
        self.pauseAnimation = True

        # Init snake
        self.snake = Snake(self.controller.config['WIDTH']/2, self.controller.config['HEIGHT']/2)

        # Init food
        self.foods = pygame.sprite.Group()
        self.foodArea = []

        # Init food timer
        self.SPAWN_FOOD = pygame.USEREVENT + 1
        self.allowSpawnFood = True
        pygame.time.set_timer(self.SPAWN_FOOD, 2000)

        self.background = get_image('assets/level1/back.png')
        
        self.main_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 13)
        self.stage_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 15)

        self.showObstacles = False
        self.obstacles = []
        self.objects = []


    def onLoad(self):
        self.restart()

    def isWin(self):
        return self.snake.stage == len(self.snake.stages)-1

    def restart(self):
        self.__init__(self.slug, self.level, self.controller)

    def pause(self):
        self.isPause = True
        self.snake.stop()
        self.foods.empty()

    def baseEvents(func):
        def wrapper(self, event):
            if self.isPause: return
            # Foods
            if event.type == self.SPAWN_FOOD and self.allowSpawnFood:
                Food(self.foods, self.controller, self.foodArea)

            # Snake
            self.snake.events(event)

            # Obstacles
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                self.showObstacles = not self.showObstacles

            func(self, event)
        return wrapper

    def baseUpdate(func):
        def wrapper(self):

            # Foods
            if not self.isPause: self.foods.update()

            # Snake
            if not self.isPause: self.snake.update()

            # Objects
            for obj in self.objects:
                obj.update()

            func(self)
            if self.isPause: return

            # Check collide with level obstacles
            obsCollide = pygame.Rect.collidelist(self.snake.get_rect(), self.obstacles)
            if obsCollide != -1:
                self.snake.collide()

            # Check collide snake with food
            foodCollide = pygame.Rect.collidelist(self.snake.get_rect(), [x.get_rect() for x in self.foods.sprites()])
            if foodCollide != -1:
                food = self.foods.sprites()[foodCollide]
                self.snake.grow()
                self.score += food.weight
                self.foods.remove(food)
                Food(self.foods, self.controller, self.foodArea)

                if food.slug == 'ghost':
                    self.snake.giveGhostEffect()

            # If snake collide
            if self.snake.isCollide:
                self.pause()
                self.controller.defeat()

            # Change stage
            if self.score != 0 and self.score >= (self.snake.stage+1) * self.controller.config['SCORE_TARGET']:
                # win stage
                if self.isWin():
                    self.controller.win()
                    self.snake.stop()
                    self.pause()
                    
                # next stage
                elif self.snake.speed < 5:
                    self.snake.speed += 0.5
                    self.snake.nextStage()

        return wrapper

    def baseRender(func):
        def wrapper(self, screen):
            # Background
            screen.blit(self.background, (0, 0))

            # Foods
            self.foods.draw(screen)

            # Snake
            self.snake.render(screen)

            # Objects
            for obj in self.objects:
                obj.render(screen)

            func(self, screen)

            # GUI
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 800, 45))
            screen.blit(get_image('assets/score.png'), (20, 17))

            score_label = self.main_font.render(str(self.score), True, (86, 77, 0))
            stage = self.stage_font.render(self.snake.getStageName(), True, self.snake.getStageColor())

            screen.blit(score_label, (100, 17))
            screen.blit(stage, stage.get_rect(center=(800/2, 22)))

            # Obstacles
            if self.showObstacles:
                for obs in self.obstacles:
                    pygame.draw.rect(screen, (255, 0, 0), obs)
            
        return wrapper

    @baseEvents
    def events(self, event): pass

    @baseUpdate
    def update(self): pass

    @baseRender
    def render(self, screen): pass

class Level1(Level):
    def __init__(self, slug, level, controller):
        super().__init__(slug, level, controller)

        self.obstacles = [
            pygame.Rect(187, 171, 109, 52),
            pygame.Rect(573, 264, 118, 68),
            pygame.Rect(156, 455, 103, 60)
        ]
        self.objects = [
            Object(184, 152, 'assets/level1/obs1.png'),
            Object(573, 211, 'assets/level1/obs2.png'),
            Object(149, 451, 'assets/level1/obs3.png'),
        ]
        
class Level2(Level):
    def __init__(self, slug, level, controller):
        super().__init__(slug, level, controller)
        
        self.background = get_image('assets/level2/back.png')

        self.obstacles = [
            pygame.Rect(78, 211, 176, 33),
            pygame.Rect(131, 267, 56, 63),
            pygame.Rect(205, 272, 35, 50),
            pygame.Rect(508, 239, 166, 28),
            pygame.Rect(508, 366, 166, 28),
            pygame.Rect(667, 516, 68, 47),
        ]
        self.objects = [
            Object(78, 75, 'assets/level2/obs1.png'),
            Object(340, 43, 'assets/level2/obs2.png'),
            Object(126, 263, 'assets/level2/obs3.png'),
            Object(202, 254, 'assets/level2/obs4.png'),
            Object(656, 424, 'assets/level2/obs5.png'),
            Object(490, 194, 'assets/level2/obs6.png'),
        ]

class Level3(Level):
    def __init__(self, slug, level, controller):
        super().__init__(slug, level, controller)

        self.background = get_image('assets/level3/back.png')

        self.snake = Snake(87, 520)

        self.emitter = ProjectileEmitter(723, 247, get_image('assets/level3/cannon.png'), 'level3\projectile')

        self.foodArea = [
            pygame.Rect(153, 274, 132, 43),
            pygame.Rect(309, 204, 132, 150),
            pygame.Rect(569, 333, 82, 157),
            pygame.Rect(22, 202, 118, 51),
            pygame.Rect(31, 419, 133, 140),
        ]
        self.obstacles = [
            pygame.Rect(486, 263, 43, 14),
            pygame.Rect(548, 518, 122, 82),
            pygame.Rect(277, 385, 271, 215),
            pygame.Rect(193, 333, 84, 267),
            pygame.Rect(0, 588, 193, 12),
            pygame.Rect(0, 402, 8, 186),
            pygame.Rect(0, 66, 8, 207),
            pygame.Rect(0, 273, 126, 129),
            pygame.Rect(320, 160, 38, 14),
            pygame.Rect(130, 172, 38, 14),
            pygame.Rect(193, 66, 79, 190),
            pygame.Rect(670, 45, 130, 555),
            pygame.Rect(-1, 45, 671, 21),
            pygame.Rect(33, 142, 34, 14),
        ]
        self.objects = [
            Object(97, 365, 'assets/level3/obs1.png'),
            Object(315, 135, 'assets/level3/obs2.png'),
            Object(126, 150, 'assets/level3/obs3.png'),
            Object(0, 22, 'assets/level3/obs4.png'),
            AnimatedObject(121, 52, 'level3/flag', 4, 10),
            AnimatedObject(430, 0, 'level3/tree', 3, 40, loop=True),
        ]

    @Level.baseUpdate
    def update(self):
        self.emitter.update()

        projCollide = pygame.Rect.collidelist(self.snake.get_rect(), [x.get_rect() for x in self.emitter.projectiles.sprites()])
        if projCollide != -1:
            self.snake.collide()

    @Level.baseRender
    def render(self, screen):
        self.emitter.render(screen)


class Level4(Level):
    def __init__(self, slug, level, controller):
        super().__init__(slug, level, controller)
        
        self.snake = Snake(101, 450)
        self.background = get_image('assets/level4/back.png')


        self.foodArea = [
            (pygame.Rect(599, 420, 141, 102), 'ghost'),
            (pygame.Rect(79, 200, 145, 102), 'ghost'),
            pygame.Rect(79, 318, 304, 196),
            pygame.Rect(477, 232, 250, 178),
        ]
        self.obstacles = [
            pygame.Rect(401, 173, 46, 400),
            pygame.Rect(764, 0, 36, 573),
            pygame.Rect(0, 173, 40, 400),
            pygame.Rect(0, 0, 764, 173),
            pygame.Rect(0, 573, 800, 27),
            pygame.Rect(488, 485, 61, 15),
            pygame.Rect(685, 197, 56, 18),
            pygame.Rect(477, 200, 79, 15),
        ]
        self.objects = [
            Object(0, 533, 'assets/level4/bottom_wall.png'),
            AnimatedObject(40, 106, 'level4/fire', 24, 5),
        ]

import math
class Level5(Level):
    def __init__(self, slug, level, controller):
        super().__init__(slug, level, controller)

        self.snake = Snake(101, 450)
        self.snake.withHelmet = True
        self.background = get_image('assets/level5/back1.png')
        self.objects = [
            Enemy(400, 200, 'level5/ship', 8, 4)
        ]
        self.stage = 1

        self.portal = AnimatedObject(664, 71, 'level5/portal', 9, 5, scale=0)
        self.portalActive = False
        self.showFinal = False

        self.time = 0

        # Asters
        self.asters = pygame.sprite.Group()
        self.lastTick = pygame.time.get_ticks()

    def isWin(self):
        return False

    def spawnAster(self):
        aster = Aster()
        self.asters.add(aster)

    @Level.baseRender
    def render(self, screen):
        if self.stage == 1:
            for aster in self.asters:
                aster.render(screen)

        self.portal.render(screen)
    
    @Level.baseUpdate
    def update(self):
        self.time += 1

        self.portal.update()

        if self.stage == 1:
            now = pygame.time.get_ticks()
            if now - self.lastTick >= 4000:
                for i in range(randint(1, 3)):
                    self.spawnAster()
                self.lastTick = now

            for aster in self.asters:
                aster.update()

            asterCollide = pygame.Rect.collidelist(self.snake.get_rect(), [*[x.get_rect() for x in self.asters.sprites()], self.objects[0].get_rect()])
            if asterCollide != -1:
                self.snake.collide()

        if self.stage == 2:
            if self.showFinal and self.time % 10 and self.portal.scale < 40:
                self.portal.scale += 0.2

                if round(self.portal.scale, 1) == 30.2:
                    self.controller.win()

            artifactCollide = pygame.Rect.collidelist(self.snake.get_rect(), [self.objects[0].get_rect()])    
            if artifactCollide != -1:
                self.showFinal = True
                self.pause()

        if self.snake.stage == 5:
            self.portalActive = True

        if self.portalActive and self.time % 10 and self.portal.scale < 1:
            self.portal.scale += 0.05

        if self.stage == 1 and self.portalActive:
            portalCollide = pygame.Rect.collidelist(self.snake.get_rect(), [pygame.Rect(707, 94, 34, 78)])
            if portalCollide != -1:
                self.stage = 2
                self.snake.teleportTo(95, 124)
                    
                self.background = get_image('assets/level5/back2.png')
                self.portal = AnimatedObject(0, 67, 'level5/portal', 9, 5, angle=180)
                self.objects = [
                    AnimatedObject(694, 512, 'level5/artifact', 8, 5),
                ]
                self.obstacles = [
                    pygame.Rect(281, 135, 96, 70),
                    pygame.Rect(433, 152, 43, 38),
                    pygame.Rect(476, 167, 51, 19),
                    pygame.Rect(533, 147, 92, 80),
                    pygame.Rect(625, 227, 55, 39),
                    pygame.Rect(685, 238, 55, 39),
                    pygame.Rect(740, 215, 60, 39),
                    pygame.Rect(200, 49, 60, 39),
                    pygame.Rect(79, 337, 50, 32),
                    pygame.Rect(263, 296, 44, 31),
                    pygame.Rect(267, 243, 19, 15),
                    pygame.Rect(283, 444, 19, 15),
                    pygame.Rect(333, 293, 72, 27),
                    pygame.Rect(461, 301, 47, 34),
                    pygame.Rect(522, 333, 37, 34),
                    pygame.Rect(486, 357, 37, 61),
                    pygame.Rect(523, 374, 23, 29),
                    pygame.Rect(469, 373, 17, 30),
                    pygame.Rect(462, 411, 17, 13),
                    pygame.Rect(477, 432, 17, 13),
                    pygame.Rect(465, 454, 17, 14),
                    pygame.Rect(415, 459, 44, 38),
                    pygame.Rect(343, 468, 47, 14),
                    pygame.Rect(330, 482, 74, 43),
                    pygame.Rect(394, 525, 61, 37),
                    pygame.Rect(142, 418, 104, 52),
                    pygame.Rect(599, 424, 99, 30),
                    pygame.Rect(660, 358, 36, 57),
                    pygame.Rect(696, 369, 20, 38),
                    pygame.Rect(646, 374, 14, 33),
                    pygame.Rect(593, 454, 94, 30),
                    pygame.Rect(609, 484, 62, 20),
                    pygame.Rect(142, 470, 86, 24),
                    pygame.Rect(404, 515, 36, 10),
                    pygame.Rect(379, 562, 49, 38),
                    pygame.Rect(344, 280, 47, 13),
                    pygame.Rect(344, 320, 47, 13),
                ]

        elif self.stage == 2 and self.portalActive:
            portalCollide = pygame.Rect.collidelist(self.snake.get_rect(), [pygame.Rect(43, 88, 34, 78)])
            if portalCollide != -1:                    
                self.stage = 1
                self.snake.teleportTo(695, 131)
                self.foods.empty()
                self.allowSpawnFood = False

                self.portal = AnimatedObject(664, 71, 'level5/portal', 9, 5)
                self.background = get_image('assets/level5/back1.png')
                self.objects = [
                    Enemy(400, 200, 'level5/ship', 8, 4)
                ]
            