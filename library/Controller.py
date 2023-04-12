from .views import DefeatPopup, WinPopup
from .db.db import update_user

class Controller():
    def __init__(self, startView, config):
        self.activeView = startView
        self.config = config

        self.views = []
        self.popups = []

        self.user = {}
        self.game = True
        self.status = 'playing'

    def setViews(self, views):
        self.views = views

    def setPopups(self, popups):
        self.popups = popups

    def getActiveView(self):
        for view in self.views:
            if view.slug == self.activeView: return view

    def getPopupBySlug(self, slug):
        for popup in self.popups:
            if popup.slug == slug: return popup

    def changeView(self, slug):
        self.activeView = slug
        self.getActiveView().onLoad()
        print('Change View', slug)

    def activatePopup(self, slug):
        self.getPopupBySlug(slug).activate()

    def deactivatePopup(self, slug):
        self.getPopupBySlug(slug).deactivate()


    def update(self):
        for view in self.views:
            if view.slug == self.activeView: view.update()
        
        for popup in self.popups:
            if popup.active: popup.update()

    def render(self, screen):
        for view in self.views:
            if view.slug == self.activeView: view.render(screen)

        for popup in self.popups:
            if popup.active: popup.render(screen)

    def events(self, event):
        for view in self.views:
            if view.slug == self.activeView: view.events(event)

        for popup in self.popups:
            if popup.active: popup.events(event)


    def defeat(self):
        self.activatePopup('defeat')

    def win(self):
        level = self.getActiveView().level
        if self.user['max_lvl'] == level:
            self.user['max_lvl'] += 1
            update_user(self.user['id'], self.user['max_lvl'])
            print('Update user: ', self.user)

        self.activatePopup('win')

    def restart(self):
        self.getActiveView().restart()

    def pause(self):
        pass

    def resume(self):
        pass
        
