from os import sep
from random import choice, randint
from time import sleep

import pygame

# Images
_image_library = {}
def get_image(path):
        global _image_library
        img = _image_library.get(path)
        if img == None:
                canonicalized_path = path.replace('/', sep).replace('\\', sep)
                img = pygame.image.load(canonicalized_path).convert_alpha()
                _image_library[path] = img
        return img

def rotate(image, angle, x = 0, y = 0):
    rotated_image = pygame.transform.rotate(image, angle)

    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = (x, y)).center)

    return rotated_image, new_rect

def checkInSnake(parts, radius = 15, x = -1, y = -1):
    for p_x, p_y in parts:
        if x != -1:
            if p_x - radius < x and x < p_x + radius:
                return True
        if y != -1:
            if p_y - radius < y and y < p_y + radius:
                return True
    return False


from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Error")
    return db


COLOR_ACTIVE = (255, 241, 117)
COLOR_INACTIVE = (255, 246, 169)
class InputBox:
    def __init__(self, x, y, w, h, font, fontColor, text='', maxSymbols = 0, outline = True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = fontColor
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.font = font
        self.maxSymbols = maxSymbols
        self.outline = outline

    def handle_event(self, event):
        if len(self.text) > 9: return

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            #self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.maxSymbols != 0 and len(self.text) >= self.maxSymbols: return
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        #width = max(200, self.txt_surface.get_width()+10)
        #self.rect.w = width
        pass

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+25, self.rect.y+18))
        # Blit the rect.
        if self.outline:
            pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, rect, image, hover_image = None, active_image = None, onClick = None):
        self.rect = rect
        self.image = image
        self.hover_image = hover_image
        self.active_image = active_image

        self.onClick = onClick

        self.isHover = False
        self.isPressed = False
        self.isDisabled = False

    def events(self, event, params = {}):
        if self.isDisabled: return
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.isHover = True

            if event.type == pygame.MOUSEBUTTONUP and self.isPressed:
                if (self.onClick is not None):
                    self.onClick(params)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.isPressed = True
            else: self.isPressed = False

        else: self.isHover = False

    def render(self, screen):
        image = self.image
        if (self.isHover and self.hover_image): image = self.hover_image
        if (self.isPressed and self.active_image): image = self.active_image
        screen.blit(get_image(image), self.rect)

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = get_image(image)

    def update(self): pass

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, x, y, path, framesNumber, animationSpeed, loop = False, angle = 0, isForward = False, scale = 1):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.path = path
        self.animationSpeed = animationSpeed
        self.frames = []
        self.active_frame = 1
        self.loop = loop
        self.angle = angle
        self.scale = scale

        self.isForward = isForward
        self.isReverse = False

        for i in range(1, framesNumber+1):
            frame, rect = rotate(get_image(f"assets/{path}/{i}.png"), self.angle)
            self.frames.append(frame)
            self.rect = frame.get_rect(x=x, y=y)

    def update(self):

        if self.loop:
            if self.isReverse: self.active_frame -= 1 / self.animationSpeed
            else: self.active_frame += 1 / self.animationSpeed

            if (int(self.active_frame) < 1):
                self.isReverse = False
                self.active_frame = 1

            if (int(self.active_frame) > len(self.frames)):
                self.isReverse = True
                self.active_frame = len(self.frames)

        else:
            self.active_frame += 1 / self.animationSpeed
            if (int(self.active_frame) > len(self.frames)):
                if self.isForward: self.active_frame =  len(self.frames)
                else: self.active_frame = 1

    def render(self, screen):
        frame = self.frames[int(self.active_frame) - 1]
        rect = (self.x, self.y)
        
        w, h = self.rect.width, self.rect.height
        if self.scale != 1:
            frame = pygame.transform.scale(frame, (w * self.scale, h * self.scale))
            rect = (self.x + (w * (1-self.scale))/2, self.y + (h * (1-self.scale))/2 )
            
        screen.blit(frame, rect)

    def get_rect(self):
        return self.rect
    
class Saw(Object):
    def __init__(self, x, y, range, speed = 5):
        super().__init__(x, y, 'assets/level4/saw.png')
        self.range = range
        self.speed = speed
        self.dx = 1

    def update(self):
        if self.x >= self.range[1]: self.dx = -1
        elif self.x <= self.range[0]: self.dx = 1
        self.x += self.dx * self.speed

    def get_rect(self):
        return self.image.get_rect(x=self.x, y=self.y)

class ProjectileEmitter:
    def __init__(self, x, y, image, projectilesPath):
        self.x = x
        self.y = y
        self.shootSpeed = 100

        self.projectiles = pygame.sprite.Group()
        self.last = pygame.time.get_ticks()
        self.cooldown = 3500
        self.image = image
        self.projectilesPath = projectilesPath

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            proj = Projectile(self.x + 20, self.y + 50, 28, 17, 'level3\projectile', 4, 10 )
            self.projectiles.add(proj)

        for pro in self.projectiles:
            pro.update()

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for pro in self.projectiles:
            pro.render(screen)

class Projectile(AnimatedObject):
    def __init__(self, x, y, width, height, path, framesNumber, animationSpeed, loop = False):
        self.speed = 3
        self.width = width
        self.height = height
        super().__init__(x, y, path, framesNumber, animationSpeed, loop)

    def update(self):
        super().update()
        self.x -= self.speed
        if self.x < -50: self.kill()

    def render(self, screen):
        super().render(screen)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

import math


class Enemy(AnimatedObject):
    def __init__(self, x, y, path, framesNumber, animationSpeed, loop=False, angle=0, isForward=False):
        super().__init__(x, y, path, framesNumber, animationSpeed, loop, angle, isForward)
        self.angle = 45

        self.angleTarget = 45
        self.changeTargetDelay = randint(80, 100)
        
        self.dx = 0
        self.dy = 0
        self.ticks = 0

        self.edgeOffset = 100

    def update(self):
        super().update()

        # if self.ticks % self.changeTargetDelay == 0:
        #     self.angleTarget = randint(0, 360)
        #     self.changeTargetDelay = randint(300, 400)
        #     print(self.angleTarget)

        if self.y + self.edgeOffset < 0 or self.y > 600 + self.edgeOffset:
            self.angle = 180-self.angle
            
        if self.x + self.edgeOffset < 0 or self.x > 800 + self.edgeOffset:
            self.angle = 360-self.angle
        
        # if self.angleTarget - self.angle > 0:
        #     self.angle += 4
        # elif self.changeTargetDelay - self.angle < 0:
        #     self.angle -= 4

        self.dx = -round(math.sin(math.radians(self.angle)), 2)
        self.dy = -round(math.cos(math.radians(self.angle)), 2)

        self.x += self.dx * 5
        self.y += self.dy * 5

        self.ticks += 1

    def render(self, screen):
        frame, rect = rotate(self.frames[int(self.active_frame) - 1], self.angle, self.x, self.y)
        self.rect = rect.inflate(-45, -45)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, width=2)
        screen.blit(frame, rect)

    def get_rect(self):
        return self.rect


class Aster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        aster_image = choice(['big1', 'big2', 'med1', 'med2', 'med3', 'med4', 'small1', 'small2', 'tiny1', 'tiny2', 'tiny3'])
        self.image = get_image(f'assets/level5/aster/{aster_image}.png')

        self.x = randint(-100, 900)
        self.y = choice([randint(-200, -100), randint(700, 800)])

        self.rect = self.image.get_rect(x=self.x, y=self.y)

        self.speed = randint(10, 20) / 10
        self.angle = 0
        self.last = pygame.time.get_ticks()

        # calculate vector of speed to random center
        self.dx = randint(300, 500) - self.x
        self.dy = randint(200, 400) - self.y

        vec_len = math.sqrt(self.dx ** 2 + self.dy ** 2)
        self.dx /= vec_len
        self.dy /= vec_len

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last >= 10000:
            self.kill()

        if self.angle >= 360: self.angle = 0
        else: self.angle += self.speed

        self.x += self.dx * self.speed * 2
        self.y += self.dy * self.speed * 2

    def render(self, screen):
        frame, rect = rotate(self.image, self.angle, self.x, self.y)
        self.rect = rect.inflate(-20, -20)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, width=2)
        screen.blit(frame, rect)

    def get_rect(self):
        return self.rect