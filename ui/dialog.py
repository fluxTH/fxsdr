import pygame

from ui import UIComponentBase, UIPressable
from ui.utils import fill, render_text, get_font


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
    thickness = 0

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

class DialogButtonRowFooter(DialogComponentBase):

    buttons = []
    dialog = None

    def __init__(self, dialog, *args, **kwargs):
        super(DialogButtonRowFooter, self).__init__(*args, **kwargs)
        self.buttons = []
        self.dialog = dialog

        res = (dialog.win_width(), dialog.FOOTER_HEIGHT)
        self.surface = pygame.Surface(res)

    def loc_conv_footer(self, loc):
        return (loc[0], loc[1]-self.dialog.content_height()+self.surface.get_height())

    def add_button(self, button):
        if not button in self.buttons:
            self.buttons.append(button)

    def internal_render(self, screen):
        if len(self.buttons) < 1:
            return

        btn_width = self.surface.get_width() / len(self.buttons)

        for k, button in enumerate(self.buttons):
            if not button.width() == btn_width:
                button.set_size((btn_width, self.surface.get_height()))

            button.render(screen, (k*btn_width, 0))

    def render(self, screen, loc):
        self.location = loc

        self.internal_render(self.surface)
        screen.blit(self.surface, loc)

    def register_event(self, event, loc, *args, **kwargs):
        for button in self.buttons:
            getattr(button, event)(self.loc_conv_footer(loc), *args, **kwargs)

    def press(self, loc):
        self.register_event('press', loc)

    def drag(self, loc):
        self.register_event('drag', loc)

    def lift(self, loc):
        self.register_event('lift', loc)

class DialogTextBody(DialogComponentBase):
    
    BG_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 255)
    SHADOW_COLOR = (0, 0, 0)

    body_text = ''

    def __init__(self, res, *args, **kwargs):
        super(DialogTextBody, self).__init__(*args, **kwargs)
        self.surface = pygame.Surface(res)
        self.body_text = ''

    def set_body_text(self, text):
        self.body_text = text

    def internal_render(self, screen):
        screen.fill(self.BG_COLOR)

        text_size = 18

        lines = self.body_text.split('\n')
        line_height = get_font(size=text_size).get_linesize()

        block_height = len(lines)*line_height
        block_pad = (self.surface.get_height()-block_height)/2

        for k, line in enumerate(lines):
            label = render_text(line, size=text_size, fg=self.TEXT_COLOR, bg=None)
            label_pos = (
                (self.surface.get_width()-label.get_width())/2, 
                k*line_height+block_pad
            )

            shadow = render_text(line, size=text_size, fg=self.SHADOW_COLOR, bg=None)
            shadow_pos = (label_pos[0]+1, label_pos[1]+1)

            screen.blits(blit_sequence=(
                (shadow, shadow_pos),
                (label, label_pos)
            ))

    def render(self, screen, loc):
        self.internal_render(self.surface)
        screen.blit(self.surface, loc)

