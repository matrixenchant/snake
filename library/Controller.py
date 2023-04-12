from .views import DefeatPopup, WinPopup

class Controller():
    def __init__(self, startView, config):
        self.activeView = startView
        self.config = config

        self.popup = None
        self.views = []
        self.popups = {}

        self.user = {}
        self.game = True
        self.fps = config['FPS']
        self.status = 'playing'
        self.score = 0

    def setViews(self, views):
        self.views = views

    def setPopups(self, popups):
        self.popups = popups

    def changeView(self, slug):
        self.activeView = slug
        print('Change View', slug)

    def update(self):
        for view in self.views:
            if view.slug == self.activeView: view.update()
        
        if self.popup is not None: self.popup.update()

    def render(self, screen):
        for view in self.views:
            if view.slug == self.activeView: view.render(screen)

        if self.popup is not None: self.popup.render(screen)

    def events(self, event):
        for view in self.views:
            if view.slug == self.activeView: view.events(event)

        if self.popup is not None: self.popup.events(event)


    def defeat(self):
        self.status = 'defeat'
        self.popup = self.popups['defeat']

    def restart(self):
        self.score = 0
        FPS = 160
        game = True

    def pause(self):
        pass

    def resume(self):
        pass
        
