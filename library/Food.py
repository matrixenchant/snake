import pygame
import time
from random import randint

food_variants = [
    ['assets/food.png', 1],
    ['assets/food2.png', 3]
]

class Food(pygame.sprite.Sprite):
    def __init__(self, group, controller, spawnArea):
        pygame.sprite.Sprite.__init__(self)
        self.controller = controller

        self.width = 20
        self.height = 25

        self.spawnArea = spawnArea

        variant = food_variants[randint(0,1)]
        self.image = pygame.image.load(variant[0])
        self.weight = variant[1]

        self.rect = self.image.get_rect()
        self.is_update = True
        self.spawnTime = int(time.time())


        self.add(group)
        self.spawn()


    def spawn(self):
        x, y = 0, 0

        if len(self.spawnArea):
            rect = self.spawnArea[randint(0, len(self.spawnArea)-1)]
            print(rect)
            x = randint(rect.x, rect.x + rect.width - self.width)
            y = randint(rect.y, rect.y + rect.height - self.height)
        else:
            x = randint(self.width+10, self.controller.config['WIDTH'] - self.width-10)
            y = randint(50, self.controller.config['HEIGHT'] -self.height-10)
            
        

        self.rect.x = x
        self.rect.y = y

    def update(self):
        if not self.is_update: return
        if int(time.time()) - self.spawnTime > 5:
            self.kill()

    def get_rect(self):
        return self.rect