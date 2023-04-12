import pygame

from .db.db import add_user, get_users
from .utils import Button, InputBox, get_image

MAIN_BLACK = (50, 45, 0)

class Popup:
    def __init__(self, contoller):
        self.controller = contoller

    def events(self, event): pass
    def update(self): pass
    def render(self, screen): pass


class GUIPopup(Popup):
    def __init__(self, contoller):
        super().__init__(contoller)
        self.main_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 13)
        self.stage_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 15)

    def render(self, screen, score, stage_name, stage_color):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 800, 45))
        screen.blit(get_image('assets/score.png'), (20, 17))

        score_label = self.main_font.render(str(score), True, (86, 77, 0))
        stage = self.stage_font.render(stage_name, True, stage_color)

        screen.blit(score_label, (100, 17))
        screen.blit(stage, stage.get_rect(center=(800/2, 15)))


class WinPopup(Popup):
    def events(self, event):
        print(event)

    def render(self, screen):
        screen.blit(get_image('assets/win.png'), (111, 117))

class DefeatPopup(Popup):
    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            print('restart')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            print('menu')

    def render(self, screen):
        screen.blit(get_image('assets/game_over.png'), (215, 206))


class View:
    def __init__(self, slug, controller):
        self.slug = slug
        self.controller = controller

    def update(self): pass
    def render(self, screen): pass


class StartGame(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)

        self.btn = Button(
            rect=pygame.Rect(221, 300, 318, 85),
            image='assets/intro/start.png',
            active_image='assets/intro/start_pressed.png',
            onClick = lambda x: self.controller.changeView('users')
        )

    def events(self, event):
        self.btn.events(event)
            

    def render(self, screen):
        screen.blit(get_image('assets/logo.png'), (287, 101))
        self.btn.render(screen)


class Accounts(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)

        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.font2 = pygame.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.hoverIndex = 0
        self.isHover = False

        users = get_users()
        self.users_rect = []
        ini_y = 162
        x = 149

        def choiceUserHandler(user):
            self.controller.user['id'] = user['id']
            self.controller.user['name'] = user['name']
            self.controller.user['max_lvl'] = user['max_lvl']
            self.controller.changeView('levels')
        
        for i in range(len(users)):
            y = ini_y + 75 * i

            self.users_rect.append({
                'btn': Button(pygame.Rect(x, y, 502, 61),
                              'assets/accounts/acc_rect.png',
                              'assets/accounts/acc_rect_hover.png',
                              onClick=choiceUserHandler),
                'id': users[i][0],
                'name': users[i][1],
                'max_lvl': users[i][2],
            })

        def createNewUser(params):
            self.controller.changeView('newUser')

        self.createUserBtn = Button(
            pygame.Rect(x, ini_y + 75 * len(users), 502, 61),
            'assets/accounts/create.png',
            'assets/accounts/create_hover.png',
            onClick=createNewUser)

    def events(self, event):
        for user in self.users_rect:
            user['btn'].events(event, user)

        self.createUserBtn.events(event)

    def render(self, screen):

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/accounts/title.png'), (257, 111))

        i = 0
        for user in self.users_rect:
            name_label = self.font.render(user['name'], True, MAIN_BLACK)
            level_label = self.font2.render(str(user['max_lvl']) + ' lvl', True, (47, 131, 50))
            
            user['btn'].render(screen)
            rect = user['btn'].rect
            screen.blit(name_label, (rect.x + 25, rect.y + 18))
            screen.blit(level_label, (rect.x + 300, rect.y + 20))
            i += 1

        self.createUserBtn.render(screen)


class NewAccount(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)

        def createBtnHandler(params):
            id = add_user((self.input.text, 1))
            self.controller.user['id'] = id
            self.controller.user['name'] = self.input.text
            self.controller.user['max_lvl'] = 1
            print('New user '+str(id))

        self.createBtn = Button(
            pygame.Rect(149, 255, 502, 61),
            'assets/new_account/btn.png',
            'assets/new_account/btn_hover.png',
            onClick=createBtnHandler)

        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)

        self.input = InputBox(149, 162, 502, 61, self.font, MAIN_BLACK, 'Your name', 12, False)

    def events(self, event):
        self.input.handle_event(event)
        self.createBtn.events(event)
    
    def update(self):
        self.input.update()

    def render(self, screen):

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/new_account/title.png'), (248, 111))

        if self.input.active: screen.blit(get_image('assets/new_account/input_active.png'), (149, 162))
        else: screen.blit(get_image('assets/new_account/input.png'), (149, 162))
        self.input.draw(screen)

        self.createBtn.render(screen)


class Levels(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)

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

    def events(self, event):
        i = 0
        for lvl in self.levels:
            if lvl.collidepoint(pygame.mouse.get_pos()) and self.blockIndex != i:
                self.hoverIndex = i
                self.isHover = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.controller.changeView(f'level{i+1}')

            elif self.isHover and self.hoverIndex == i: self.isHover = False
            i+=1
    

    def render(self, screen):

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/levels/title.png'), (276, 111))

        for i, lvl in enumerate(self.levels):
            screen.blit(get_image(f'assets/levels/level{i+1}.png'), (lvl.x, lvl.y))

            if i+1 > self.controller.user['max_lvl']:
                self.blockIndex = i
                screen.blit(get_image('assets/levels/block.png'), (lvl.x, lvl.y))
            elif self.isHover and self.hoverIndex == i:
                screen.blit(get_image(f'assets/levels/play.png'), (lvl.x, lvl.y))


class Level:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False
        self.obsRects = []
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True

    def draw(self, screen):
        if not self.visible: return

    def drawObs(self, screen):
        if not self.visible: return


class Level1:
    def __init__(self, controller):
        self.controller = controller
        self.visible = False

        self.obsRects = [
            pygame.Rect(187, 171, 109, 52),
            pygame.Rect(573, 264, 118, 68),
            pygame.Rect(156, 455, 103, 60)
        ]
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True

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
            ProjectileEmitter(723, 247, get_image('assets/level3/cannon.png'), 'level3\projectile')
        ]

        snake.startPos = [87, 491]
    
    def update(self, active_view):
        if active_view != self.controller:
            self.visible = False
        else: self.visible = True



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


