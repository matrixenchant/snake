import pygame
import time
from random import randint

food_variants = [
    ['assets/food.png', 1],
    ['assets/food2.png', 3]
]

class Food(pygame.sprite.Sprite):
    def __init__(self, snake, group, controller):
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
        self.controller = controller

    def spawn(self):
        x = randint(self.width+10, self.controller.config['WIDTH'] - self.width-10)
        y = randint(50, self.controller.config['HEIGHT'] -self.height-10)

        self.x = x
        self.y = y
        self.rect = self.image.get_rect(x = x, y = y)

    def update(self):
        if not self.is_update: return
        if int(time.time()) - self.spawnTime > 5:
            self.kill()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)