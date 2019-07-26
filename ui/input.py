import pygame

from ui import UIComponentBase, UIPressable, UIException
from ui.utils import render_text, align


class InputBase(UIComponentBase):
    pass

class Button(InputBase, UIPressable):

    BTN_COLOR = (0x30, 0x30, 0x30)
    BTN_EDGE_COLOR = (0x25, 0x25, 0x25)

    BTN_HOLD_COLOR = (0x0d, 0x66, 0x78)
    BTN_EDGE_HOLD_COLOR = (0x08, 0x48, 0x54)

    def __init__(self, text, click=None, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.text = text
        self.click_func = click

    def width(self):
        if self.surface is None:
            return None
        return self.surface.get_width()

    def height(self):
        if self.surface is None:
            return None
        return self.surface.get_height()

    def set_size(self, res):
        self.surface = pygame.Surface(res)

    def internal_render(self, screen):
        # Draw button
        btn_color = self.BTN_HOLD_COLOR if self.pressed else self.BTN_COLOR
        screen.fill(btn_color)

        label_size = 24

        btn_label = render_text(self.text, size=label_size, bg=None)
        btn_label_pos = align(btn_label.get_rect(), self.surface.get_rect())

        btn_label_shadow = render_text(self.text, size=label_size, fg=(0,0,0), bg=None)
        btn_label_shadow_pos = (
            btn_label_pos[0]+1, 
            btn_label_pos[1]+1
        )

        screen.blits(blit_sequence=(
            (btn_label_shadow, btn_label_shadow_pos),
            (btn_label, btn_label_pos)
        ))

        btn_edge_color = self.BTN_EDGE_HOLD_COLOR if self.pressed else self.BTN_EDGE_COLOR
        pygame.draw.rect(screen, btn_edge_color, self.surface.get_rect(), 5)

    def render(self, screen, loc):

        if self.surface is None:
            raise UIException('Button size not initialized.')

        self.location = loc

        self.internal_render(self.surface)
        screen.blit(self.surface, loc)

class DangerButton(Button):

    BTN_COLOR = (0x60, 0x02, 0x02)
    BTN_EDGE_COLOR = (0x42, 0x02, 0x02)

    BTN_HOLD_COLOR = (0x30, 0x02, 0x02)
    BTN_EDGE_HOLD_COLOR = (0x60, 0x02, 0x02)
