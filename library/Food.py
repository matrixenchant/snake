import pygame
import time
from random import randint, choices, choice

class FoodVariant:
    def __init__(self, slug, image, weight, chance):
        self.slug = slug
        self.image = image
        self.weight = weight
        self.chance = chance

food_variants = [
    FoodVariant('basic', 'assets/food1.png', 1, 50),
    FoodVariant('super', 'assets/food2.png', 3, 30),
    FoodVariant('ghost', 'assets/food-ghost.png', 1, 20),
]

class Food(pygame.sprite.Sprite):
    def __init__(self, group, controller, spawnArea):
        pygame.sprite.Sprite.__init__(self)
        self.controller = controller

        self.width = 20
        self.height = 25
        self.image = None
        self.weight = 0
        self.slug = ''
        self.spawnArea = spawnArea

        self.is_update = True
        self.spawnTime = int(time.time())

        self.add(group)
        self.spawn()


    def spawn(self):
        x, y = 0, 0

        basic_variants = food_variants[:2]
        chances = list(map(lambda x: x.chance, basic_variants))
        variant = choices(basic_variants, weights=chances)[0]

        if len(self.spawnArea):
            rect = choice(self.spawnArea)

            if type(rect) is tuple:
                variant = self.getVariantBySlug(rect[1])
                rect = rect[0]

            x = randint(rect.x, rect.x + rect.width - self.width)
            y = randint(rect.y, rect.y + rect.height - self.height)
        else:
            x = randint(self.width+10, self.controller.config['WIDTH'] - self.width-10)
            y = randint(50, self.controller.config['HEIGHT'] - self.height-10)

        self.image = pygame.image.load(variant.image)
        self.weight = variant.weight
        self.slug = variant.slug
            
        self.rect = self.image.get_rect(x=x, y=y)

    def getVariantBySlug(self, slug):
        for var in food_variants:
            if var.slug == slug: return var

    def update(self):
        if not self.is_update: return
        if int(time.time()) - self.spawnTime > 6:
            self.kill()

    def get_rect(self):
        return self.rect