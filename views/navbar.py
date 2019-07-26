from ui.utils import render_text, align
from ui.nav import NavButton, NavBackButton, NavFreqButton

from views import ViewBase
from views.settings import SettingsView, AboutView

from constants import *


class Navbar(ViewBase):

    BG_COLOR = (0x16, 0x16, 0x16)
    DIALOG_COLOR = (0, 0x44, 0x75)

    TITLE_FONT_SIZE = {
        SCREEN_SMALL: 20,
        SCREEN_MEDIUM: 24,
        SCREEN_LARGE: 28
    }

    def __init__(self, res, *args, **kwargs):
        super(Navbar, self).__init__(res, *args, **kwargs)
        self.rect = (0, 0, res[0], res[1])

        self.title_text = 'FxSDR'
        self.freq_btn = NavFreqButton('OFF', click=self.controller.show_alert)
        # self.freq_btn = NavFreqButton('OFF', click=self.controller.go_root)
        self.about_btn = NavButton('About', click=self.click_about)
        self.back_btn = NavBackButton('Back', click=self.controller.back)
        self.settings_btn = NavButton('Settings', click=self.click_settings)

    def click_settings(self):
        self.controller.segue(SettingsView)

    def click_about(self):
        self.controller.segue(AboutView)

    def render(self, screen):
        screen.fill(self.BG_COLOR)

        # Left Button
        if self.controller.is_view(SettingsView):
            about_btn_pos = align(self.about_btn.get_rect(), self.rect, horizontal=ALIGN_RIGHT, hpad=-15)
            self.about_btn.render(screen, about_btn_pos)
        elif not self.controller.is_view(AboutView):
            freq_btn_pos = align(self.freq_btn.get_rect(), self.rect, horizontal=ALIGN_RIGHT, hpad=-15)
            self.freq_btn.render(screen, freq_btn_pos)

        # Right Button
        if self.controller.is_root():
            settings_btn_pos = align(self.settings_btn.get_rect(), self.rect, horizontal=ALIGN_LEFT, hpad=15)
            self.settings_btn.render(screen, settings_btn_pos)
        else:
            back_btn_pos = align(self.back_btn.get_rect(), self.rect, horizontal=ALIGN_LEFT, hpad=5)
            self.back_btn.render(screen, back_btn_pos)

        # Title
        title = render_text(
            self.title_text, 
            size=self.TITLE_FONT_SIZE[self.controller.get_screen_scale()], 
            font='./assets/HelveticaNeueBold.ttf', 
            bg=None
        )
        title_pos = align(title.get_rect(), self.rect)
        screen.blit(title, title_pos)

    def register_event(self, event, *args, **kwargs):
        if event not in ['press', 'drag', 'lift']:
            return

        if self.controller.is_root():
            getattr(self.settings_btn, event)(*args, **kwargs)
        else:
            getattr(self.back_btn, event)(*args, **kwargs)

        if self.controller.is_view(SettingsView):
            getattr(self.about_btn, event)(*args, **kwargs)
        elif not self.controller.is_view(AboutView):
            getattr(self.freq_btn, event)(*args, **kwargs)

