import pygame

from views.navbar import Navbar
from views.dashboard import DashboardView
from views.dialog.alert import AlertDialog

from ui.utils import render_text

from constants import *

class FxSdrController(object):

    RootView = None
    ViewHistory = []
    NavBar = None
    Dialog = []

    screen_scale = None
    navbar_height = None
    last_interact_view = None

    s_content = None
    s_navbar = None
    s_dialog = None

    def __init__(self, app):
        self.app = app

        self.init_surfaces()

        self.init_navbar()
        self.init_rootview(DashboardView)

    # ---- Initialization methods ----

    def init_navbar(self):
        self.Navbar = Navbar(self.navbar_resolution(), self)

    def init_rootview(self, root_view):
        self.RootView = root_view(self.content_resolution(), self)

    def init_surfaces(self):
        self.s_content = pygame.Surface(self.content_resolution())
        self.s_navbar = pygame.Surface(self.navbar_resolution())
        self.s_dialog = pygame.Surface(self.app.resolution, pygame.SRCALPHA)

    # ---- Updater methods ----

    def update_navbar(self):
        title = 'FxSDR'
        if not self.is_root():
            title = self.current().title()

            if self.get_screen_scale() == SCREEN_SMALL:
                self.Navbar.back_btn.set_text('Back')
            else:
                if len(self.ViewHistory) >= 2:
                    self.Navbar.back_btn.set_text(self.ViewHistory[-2].title())
                elif len(self.ViewHistory) == 1:
                    self.Navbar.back_btn.set_text(self.RootView.title())
                else:
                    self.Navbar.back_btn.set_text('Back')

        self.Navbar.title_text = title

    # ---- View changing methods ----

    def go_root(self):
        if self.is_root():
            return False

        self.ViewHistory = []
        self.update_navbar()
        return True

    def segue(self, next_view):
        view = next_view(self.content_resolution(), self)
        self.ViewHistory.append(view)
        self.update_navbar()
        return True

    def back(self):
        if self.is_root():
            return False

        del self.ViewHistory[-1]
        self.update_navbar()

    def init_dialog(self, dialog_class):
        return dialog_class(self.app.resolution, self)

    def show_dialog(self, dialog):
        self.Dialog.append(dialog)

    def show_alert(self, title='Alert'):
        for k, i in enumerate(range(3)):
            alert = self.init_dialog(AlertDialog)
            alert.set_title(f'{title} number {i}')

            self.show_dialog(alert)

    def delete_dialog(self, dialog):
        self.Dialog.remove(dialog)

    # ---- Getter methods ----

    def get_screen_scale(self):
        if self.screen_scale is None:
            if self.app.resolution[1] < 320:
                self.screen_scale = SCREEN_SMALL
            elif self.app.resolution[1] < 480:
                self.screen_scale = SCREEN_MEDIUM
            else:
                self.screen_scale = SCREEN_LARGE

        return self.screen_scale

    def get_navbar_height(self):
        if self.navbar_height is None:
            self.navbar_height = 48 # Default
            if self.get_screen_scale() == SCREEN_SMALL:
                self.navbar_height = 36
            elif self.get_screen_scale() == SCREEN_MEDIUM:
                self.navbar_height = 48
            elif self.get_screen_scale() == SCREEN_LARGE:
                self.navbar_height = 56

        return self.navbar_height

    def navbar_resolution(self):
        return (self.app.resolution[0], self.get_navbar_height())

    def content_resolution(self):
        return (self.app.resolution[0], self.app.resolution[1] - self.get_navbar_height())

    def loc_conv_content(self, loc):
        return (loc[0], loc[1] - self.get_navbar_height())

    def in_navbar(self, loc):
        return (loc[1] <= self.get_navbar_height())

    def in_content(self, loc):
        return (loc[1] > self.get_navbar_height())

    def is_view(self, view_class):
        return self.current().__class__ is view_class

    def is_root(self):
        if len(self.ViewHistory) <= 0:
            return True
        return False

    def current(self):
        if self.is_root():
            return self.RootView
        else:
            return self.ViewHistory[-1]

    def is_dialog_present(self):
        if self.dialog_count() > 0:
            return True
        return False

    def dialog_count(self):
        return len(self.Dialog)

    def dialog(self):
        if self.is_dialog_present():
            return self.Dialog[-1]
        return False

    # ---- Event listeners ----

    def register_event(self, event, loc, *args, **kwargs):
        # Dialog
        if self.is_dialog_present():
            self.last_interact_view = self.dialog().__class__.__name__
            getattr(self.dialog(), event)(loc, *args, **kwargs)
            return

        # Normal view
        if event == 'lift':
            # TODO: Fix lift activating pressables from another view.
            getattr(self.Navbar, event)(loc, *args, **kwargs)
            getattr(self.current(), event)(self.loc_conv_content(loc), *args, *kwargs)
        else:
            if self.in_content(loc):
                self.last_interact_view = self.current().__class__.__name__
                getattr(self.current(), event)(self.loc_conv_content(loc), *args, *kwargs)
            else:
                self.last_interact_view = self.Navbar.__class__.__name__
                getattr(self.Navbar, event)(loc, *args, **kwargs)

    def m_press(self, loc):
        self.register_event('press', loc)

    def m_drag(self, loc):
        self.register_event('drag', loc)

    def m_click(self, loc):
        self.register_event('click', loc)

    def m_lift(self, loc):
        self.register_event('lift', loc)

    # ---- Rendering methods ----

    def draw_fps(self, screen):
        fps_label = render_text(
            f'{self.app.clock.get_fps():.1f} fps', 
            size=16
        )
        fps_label.set_alpha(100)
        screen.blit(fps_label, fps_label.get_rect(bottomleft=(0, self.app.resolution[1])))

    def render_current(self, screen):
        if not self.is_dialog_present():
            self.current().render(self.s_content)
            self.Navbar.render(self.s_navbar)

            seq = (
                (self.s_content, (0, self.get_navbar_height())),
                (self.s_navbar, (0, 0))
            )
        else:
            self.s_dialog.fill((0, 0, 0, 128))
            self.s_dialog.set_alpha(255)
            self.dialog().render(self.s_dialog)

            seq = (
                (self.s_content, (0, self.get_navbar_height())),
                (self.s_navbar, (0, 0)),
                (self.s_dialog, (0, 0))
            )

        # print(self.last_interact_view)

        screen.blits(blit_sequence=seq)

        if True:
            self.draw_fps(screen)



