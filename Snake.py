import random
import pygame

class Snake:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.size = 0
        self.parts = [[x, y]]
        self.radius = 10
        self.dx = 0
        self.dy = -1
        
        self.speed = 60
        self.offset_parts = 1
        self.color_body = (31, 97, 34)
        self.color_head = (47, 131, 50)
        self.liveTime = 0
        self.grow(20)

        self.isRainbow = False
        self.isGrowing = False
        self.isStopped = False
        self.isCollide = False
        self.isShow = False

    def events(self, event):
        # KEYDOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.isGrowing = True
            
            # Control
            if event.key in [pygame.K_LEFT, pygame.K_a] and self.dx != 1: self.set_direction('left')
            if event.key in [pygame.K_RIGHT, pygame.K_d] and self.dx != -1: self.set_direction('right')
            if event.key in [pygame.K_UP, pygame.K_w] and self.dy != 1: self.set_direction('up')
            if event.key in [pygame.K_DOWN, pygame.K_s] and self.dy != -1: self.set_direction('down')

    def set_direction(self, dir):
        offset = 1
        if dir == 'left':
            self.dx = -1 * offset
            self.dy = 0
        elif dir == 'right':
            self.dx = 1 * offset
            self.dy = 0
        elif dir == 'up':
            self.dx = 0
            self.dy = -1 * offset
        elif dir == 'down':
            self.dx = 0
            self.dy = 1 * offset

    def render(self, screen):
        if not self.isShow: return
        for i in range(self.size - 1, 0, -1):
            color = self.color_body
            #head
            if i < 5: color = self.color_head

            if self.isRainbow:
                pygame.draw.circle(screen, random.choices(range(256), k=3), self.parts[i], self.radius)
            else:
                pygame.draw.circle(screen, color, self.parts[i], self.radius)

    def stop(self):
        self.isStopped = True

    def resume(self):
        self.isStopped = False

    def show(self):
        self.isShow = True
    def hide(self):
        self.isShow = False

    def restart(self):
        self.isStopped = False
        self.isRainbow = False
        self.isShow = True
        self.parts = [[self.startPos[0], self.startPos[1]]]
        self.dx = 0
        self.dy = -1
        self.size = 0
        self.color_body = (31, 97, 34)
        self.color_head = (47, 131, 50)
        self.grow(20)
        self.isCollide = False

    def update(self):
        if self.isStopped: return False
        # Check grow
        if self.isGrowing: self.grow()

        # Check collision
        x = self.parts[0][0]
        y = self.parts[0][1]
        if x < self.radius or x > 800 - self.radius: print('stuck x'); self.isCollide = True
        if y < self.radius or y > 600 - self.radius: print('stuck y'); self.isCollide = True

        if self.check_self_collision() != -1: self.isCollide = True

        # Change parts
        for i in range(self.size - 1, 0, -1):
            self.parts[i][0] = self.parts[i-1][0]
            self.parts[i][1] = self.parts[i-1][1]

        # Move main part (head)
        self.parts[0][0] += self.dx * self.offset_parts
        self.parts[0][1] += self.dy * self.offset_parts


        self.liveTime += 1

    def grow(self, size = 20):
        self.size += size
        self.parts.extend(list([-100,-100] for i in range(size)))
        self.isGrowing = False

    def enableRainbow(self):
        self.isRainbow = True
    def disableRainbow(self):
        self.isRainbow = False

    def check_self_collision(self):
        body = []
        for i in range(40, self.size, 20):
            part_x = self.parts[i][0]
            part_y = self.parts[i][1]
            if part_x-self.radius != -110:
                body.append(pygame.Rect(part_x-self.radius, part_y-self.radius, self.radius*2, self.radius*2))
        return pygame.Rect.collidelist(self.get_rect(), body)

    def get_rect(self):
        head_x = self.parts[0][0]
        head_y = self.parts[0][1]
        return pygame.Rect(head_x-self.radius, head_y-self.radius, self.radius*2, self.radius*2)