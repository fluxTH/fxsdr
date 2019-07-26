import pygame

from ui import UIComponentBase, UIPressable
from ui.utils import fill, render_text


class DialogComponentBase(UIComponentBase):
    pass

class DialogWindowButton(DialogComponentBase):
    pass

class DialogCloseButton(DialogWindowButton, UIPressable):

    BG_COLOR = (150, 0, 0)
    BG_HOLD_COLOR = (90, 0, 0)
    X_COLOR = (255, 255, 255)
    X_HOLD_COLOR = (200, 200, 200)

    width = 0

    def __init__(self, width=40, thickness=4, click=None, *args, **kwargs):
        super(DialogCloseButton, self).__init__(*args, **kwargs)
        self.width = width
        self.thickness = thickness
        self.click_func = click
        self.surface = pygame.Surface((width, width))

    def internal_render(self, screen):
        # Draw button
        bg_color = self.BG_HOLD_COLOR if self.pressed else self.BG_COLOR
        screen.fill(bg_color)

        x_color = self.X_HOLD_COLOR if self.pressed else self.X_COLOR
        x_size = self.width/2
        x_start = x_size/2
        x_end = self.width-x_size/2

        # Draw X
        pygame.draw.aaline(screen, x_color, (x_start, x_start-1), (x_end, x_end), self.thickness)
        pygame.draw.aaline(screen, x_color, (x_end, x_start-1), (x_start, x_end), self.thickness)

    def render(self, screen, loc):
        self.location = loc

        # print(self.pressed, self.pressed_at)

        self.internal_render(self.surface)
        screen.blit(self.surface, loc)

