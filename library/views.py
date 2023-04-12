import pygame

from .db.db import add_user, get_users
from .utils import Button, InputBox, get_image

MAIN_BLACK = (50, 45, 0)

class View:
    def __init__(self, slug, controller):
        self.slug = slug
        self.controller = controller

    def onLoad(self): pass

    def update(self): pass
    def render(self, screen): pass

class Popup(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def events(self, event): pass
    def update(self): pass
    def render(self, screen): pass


class WinPopup(Popup):
    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.controller.deactivatePopup('win')
            self.controller.restart()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.controller.deactivatePopup('win')
            self.controller.changeView('levels')

    def render(self, screen):
        screen.blit(get_image('assets/win.png'), (111, 117))

class DefeatPopup(Popup):
    def events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.controller.deactivatePopup('defeat')
            self.controller.restart()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.controller.deactivatePopup('defeat')
            self.controller.changeView('levels')

    def render(self, screen):
        screen.blit(get_image('assets/game_over.png'), (215, 206))


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

    def onLoad(self):
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
            self.controller.changeView('levels')

        self.btns = [
            Button(
            pygame.Rect(149, 255, 502, 61),
            'assets/new_account/btn.png',
            'assets/new_account/btn_hover.png',
            onClick=createBtnHandler),

            Button(
            pygame.Rect(20, 20, 40, 40),
            'assets/back.png',
            'assets/back_hover.png',
            onClick=lambda x: self.controller.changeView('users'))
        ]
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)

        self.input = InputBox(149, 162, 502, 61, self.font, MAIN_BLACK, 'Your name', 12, False)

    def events(self, event):
        self.input.handle_event(event)
        for btn in self.btns:
            btn.events(event)
    
    def update(self):
        self.input.update()

    def render(self, screen):

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/new_account/title.png'), (248, 111))

        if self.input.active: screen.blit(get_image('assets/new_account/input_active.png'), (149, 162))
        else: screen.blit(get_image('assets/new_account/input.png'), (149, 162))
        self.input.draw(screen)

        for btn in self.btns:
            btn.render(screen)


class Levels(View):
    def __init__(self, slug, controller):
        super().__init__(slug, controller)

        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 25)
        self.isHover = False
        self.hoverIndex = 0
        self.blockIndex = -1

        self.btns = [
            Button(
            pygame.Rect(20, 20, 40, 40),
            'assets/back.png',
            'assets/back_hover.png',
            onClick=lambda x: self.controller.changeView('users'))
        ]
        
        self.levels = [
            Button(rect=pygame.Rect(104, 175, 150, 120), image='assets/levels/level1.png', onClick=lambda x: self.controller.changeView('level1') ),
            Button(rect=pygame.Rect(294, 175, 150, 120), image='assets/levels/level2.png', onClick=lambda x: self.controller.changeView('level2') ),
            Button(rect=pygame.Rect(484, 175, 150, 120), image='assets/levels/level3.png', onClick=lambda x: self.controller.changeView('level3') ),
        ]

    def events(self, event):
        for lvl in self.levels:
            lvl.events(event)

        for btn in self.btns:
            btn.events(event)

    def update(self):
        for i, lvl in enumerate(self.levels):
            if i+1 > self.controller.user['max_lvl']: lvl.isDisabled = True
            else: lvl.isDisabled = False

    def render(self, screen):

        screen.blit(get_image('assets/logo.png'), (287, 27))
        screen.blit(get_image('assets/levels/title.png'), (276, 111))

        for i, lvl in enumerate(self.levels):
            lvl.render(screen)
            x = lvl.rect.x
            y = lvl.rect.y

            if i+1 > self.controller.user['max_lvl']:
                screen.blit(get_image('assets/levels/block.png'), (x, y))
            elif lvl.isHover:
                screen.blit(get_image(f'assets/levels/play.png'), (x, y))

        for btn in self.btns:
            btn.render(screen)