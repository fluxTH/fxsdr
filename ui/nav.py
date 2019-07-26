import pygame

from ui import UIComponentBase, UIPressable
from ui.utils import fill, render_text, loc_inside

class NavbarComponentBase(UIComponentBase):
    TEXT_COLOR = (0xff, 0xff, 0xff)
    LINK_COLOR = (0xe6, 0x94, 0x10)
    LINK_HOLD_COLOR = (0x75, 0x48, 0)

class NavButton(NavbarComponentBase, UIPressable):

    size = 16
    btn_text = ''

    surface_pressed = False

    def __init__(self, text, size=16, click=None):
        self.click_func = click
        self.size = size
        self.set_text(text)

    def set_text(self, text):
        self.btn_text = text
        self.internal_render()

    def internal_render(self):
        color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
        self.surface = render_text(self.btn_text, size=self.size, fg=color, bg=None)
        self.surface_pressed = self.pressed

    def render(self, screen, loc):
        self.location = loc

        if not self.pressed == self.surface_pressed:
            self.internal_render()

        screen.blit(self.surface.convert_alpha(), loc)

class NavBackButton(NavButton):

    back_icon = None
    
    def __init__(self, text, size=16, click=None):

        self.click_func = click
        self.size = size

        self.back_icon = pygame.image.load('./assets/back.png').convert_alpha()
        self.back_icon = pygame.transform.scale(self.back_icon, (25, 25))

        self.set_text(text)

    def internal_render(self):
        color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
        text = render_text(self.btn_text, size=self.size, fg=color, bg=None)
        
        fill(self.back_icon, color)

        _, _, tw, th = text.get_rect()
        _, _, iw, ih = self.back_icon.get_rect()

        self.surface = pygame.Surface((tw+iw, max(th, ih)), pygame.SRCALPHA, 32)
        self.surface_pressed = self.pressed

        self.surface.blits(blit_sequence=(
            (self.back_icon, (0, 0)),
            (text, (iw, abs(ih-th)/2))
        ))

class NavFreqButton(NavButton):

    def __init__(self, text, size=16, click=None):

        self.click_func = click
        self.size = size

        self.set_text(text)

    def internal_render(self):
        if not self.btn_text == 'OFF':
            color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
        else:
            color = (150, 0, 0) if self.pressed else (255, 0, 0)

        self.surface = render_text(self.btn_text, size=self.size, fg=color, bg=None)
        self.surface_pressed = self.pressed

class NavText(NavbarComponentBase):
    pass

class NavTitle(NavText):
    pass