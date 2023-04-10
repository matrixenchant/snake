import pygame

from db import add_user, get_users
from utils import AnimatedObject, InputBox, get_image

MAIN_BLACK = (50, 45, 0)

USER = {}
def updateLvlUser(lvl):
    global USER
    USER['max_lvl'] = lvl

def gui(screen, stage_font, main_font, score, stage_name, stage_color):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 800, 45))
    screen.blit(get_image('assets/score.png'), (20, 17))
    score_label = main_font.render(str(score), True, (86, 77, 0))
    stage = stage_font.render(stage_name, True, stage_color)
    screen.blit(score_label, (100, 17))
    screen.blit(stage, stage.get_rect(center=(800/2, 15)))

class startGame:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.btn_pressed = False
        self.rect_btn = pygame.Rect(221, 300, 318, 85)

    def handle_event(self, event):
        if not self.visible: return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_btn.collidepoint(event.pos):
                # Toggle the active variable.
                self.btn_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and self.btn_pressed:
            self.btn_pressed = False
            return True

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/logo.png'), (287, 101))
        if self.btn_pressed:
            screen.blit(get_image('assets/intro/start_pressed.png'), (241, 315))
        else:
            screen.blit(get_image('assets/intro/start.png'), (221, 300))



class Accounts:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.rect_btn_new = pygame.Rect(0, 0, 0, 0)
        self.users_rect = []
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.font2 = pygame.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.hoverIndex = 0
        self.isHover = False
        self.users = get_users()

    def handle_event(self, event):
        if not self.visible: return False

        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect_btn_new.collidepoint(event.pos):
                return 3

        i = 0
        for btn in self.users_rect:
            if btn.collidepoint(pygame.mouse.get_pos()):
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    USER['id'] = self.users[i][0]
                    USER['name'] = self.users[i][1]
                    USER['max_lvl'] = self.users[i][2]
                    return 4

            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/accounts/title.png'), (257, 111))

        ini_y = 162
        accs = self.users
        
        self.users_rect = []
        for i in range(len(accs)+1):
            y = ini_y + 75 * i
            x = 149

            hover = ''
            if self.isHover and self.hoverIndex == i: hover = '_hover'

            if i == len(accs):
                screen.blit(get_image(f'assets/accounts/create{hover}.png'), (x, y))
            else:
                name_label = self.font.render(accs[i][1], True, MAIN_BLACK)
                level_label = self.font2.render(str(accs[i][2])+' lvl', True, (47, 131, 50))
                
                screen.blit(get_image(f'assets/accounts/acc_rect{hover}.png'), (x, y))
                screen.blit(name_label, (x + 25, y + 18))
                screen.blit(level_label, (x + 300, y + 20))

            self.users_rect.append(pygame.Rect(x, y, 502, 61))
        self.rect_btn_new = self.users_rect[len(self.users_rect)-1]



class NewAccount:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.rect_btn_create = pygame.Rect(149, 255, 502, 61)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.input = InputBox(149, 162, 502, 61, self.font, MAIN_BLACK, 'Your name', 12, False)

    def handle_event(self, event):
        if not self.visible: return False

        self.input.handle_event(event)

        if self.rect_btn_create.collidepoint(pygame.mouse.get_pos()):
            self.isHover = True
            if event.type == pygame.MOUSEBUTTONUP:
                id = add_user((self.input.text, 1))
                USER['id'] = id
                USER['name'] = self.input.text
                USER['max_lvl'] = 1
                print('New user '+str(id))
                return True
        else: self.isHover = False

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

        self.input.update()

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/new_account/title.png'), (248, 111))

        if self.input.active: screen.blit(get_image('assets/new_account/input_active.png'), (149, 162))
        else: screen.blit(get_image('assets/new_account/input.png'), (149, 162))
        self.input.draw(screen)

        hover = ''
        if self.isHover: hover = '_hover'
        screen.blit(get_image(f'assets/new_account/btn{hover}.png'), (self.rect_btn_create.x, self.rect_btn_create.y))




class Levels:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.rect_btn_create = pygame.Rect(149, 255, 502, 61)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.hoverIndex = 0
        self.blockIndex = -1
        self.levels = [
            pygame.Rect(104, 175, 150, 120),
            pygame.Rect(294, 175, 150, 120),
            pygame.Rect(484, 175, 150, 120),
        ]

    def handle_event(self, event):
        if not self.visible: return False

        i = 0
        for lvl in self.levels:
            if lvl.collidepoint(pygame.mouse.get_pos()) and self.blockIndex != i:
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    return self.controller+1+i
            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True

        print(self.blockIndex)
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/levels/title.png'), (276, 111))

        for i, lvl in enumerate(self.levels):
            screen.blit(get_image(f'assets/levels/level{i+1}.png'), (lvl.x, lvl.y))

            if i+1 > USER['max_lvl']:

                self.blockIndex = i
                screen.blit(get_image('assets/levels/block.png'), (lvl.x, lvl.y))
            if self.isHover and self.hoverIndex == i and not block:
                screen.blit(get_image(f'assets/levels/play.png'), (lvl.x, lvl.y))



class Level1:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.rect_btn_create = pygame.Rect(149, 255, 502, 61)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.hoverIndex = 0
        self.obsRects = [
            pygame.Rect(187, 171, 109, 52),
            pygame.Rect(573, 264, 118, 68),
            pygame.Rect(156, 455, 103, 60)
        ]

    def handle_event(self, event):
        if not self.visible: return False

        i = 0
        for lvl in self.levels:
            if lvl.collidepoint(pygame.mouse.get_pos()) and self.blockIndex != i:
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    return self.controller+1+i
            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/level1/back.png'), (0, 0))

    def drawObs(self, screen):
        if not self.visible: return
        
        screen.blit(get_image('assets/level1/obs1.png'), (184, 152))
        screen.blit(get_image('assets/level1/obs2.png'), (573, 211))
        screen.blit(get_image('assets/level1/obs3.png'), (149, 451))


class Level2:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.rect_btn_create = pygame.Rect(149, 255, 502, 61)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.hoverIndex = 0
        self.obsRects = [
            pygame.Rect(78, 211, 176, 33),
            pygame.Rect(131, 267, 56, 63),
            pygame.Rect(205, 272, 35, 50),
            pygame.Rect(508, 239, 166, 28),
            pygame.Rect(508, 366, 166, 28),
            pygame.Rect(667, 516, 68, 47),
        ]

    def handle_event(self, event):
        if not self.visible: return False

        i = 0
        for lvl in self.levels:
            if lvl.collidepoint(pygame.mouse.get_pos()) and self.blockIndex != i:
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    return self.controller+1+i
            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/level2/back.png'), (0, 0))

    def drawObs(self, screen):
        if not self.visible: return
        
        screen.blit(get_image('assets/level2/obs1.png'), (78, 75))
        screen.blit(get_image('assets/level2/obs2.png'), (340, 43))
        screen.blit(get_image('assets/level2/obs3.png'), (126, 263))
        screen.blit(get_image('assets/level2/obs4.png'), (202, 254))
        screen.blit(get_image('assets/level2/obs5.png'), (656, 424))
        screen.blit(get_image('assets/level2/obs6.png'), (490, 194))

class Level3:
    def __init__(self, controller, snake):
        self.controller = controller
        self.visible = False
        self.rect_btn_create = pygame.Rect(149, 255, 502, 61)
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.hoverIndex = 0
        self.obsRects = [
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
        self.animatedObjects = [
            AnimatedObject(121, 52, 'level3/flag', 4, 40),
            AnimatedObject(430, 0, 'level3/tree', 3, 80, loop=True),
        ]

        snake.startPos = [87, 491]
        

    def handle_event(self, event):
        if not self.visible: return False

        i = 0
        for lvl in self.levels:
            if lvl.collidepoint(pygame.mouse.get_pos()) and self.blockIndex != i:
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    return self.controller+1+i
            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1

        return False
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True
        
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/level3/back.png'), (0, 0))

    def drawObs(self, screen):
        if not self.visible: return

        screen.blit(get_image('assets/level3/obs2.png'), (315, 135))
        screen.blit(get_image('assets/level3/obs3.png'), (126, 150))
        screen.blit(get_image('assets/level3/obs4.png'), (0, 22))
        
        for obj in self.animatedObjects:
            obj.update(screen)

        # for obs in self.obsRects:
        #     pygame.draw.rect(screen, (255, 0, 0), obs)


