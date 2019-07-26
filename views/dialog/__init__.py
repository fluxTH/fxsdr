import pygame

from ui.utils import render_text, align, loc_inside
from ui.dialog import DialogCloseButton
from views import ViewBase

from constants import *


class DialogBase(ViewBase):
    WIN_PAD = 30
    TITLEBAR_HEIGHT = 40

    BG_COLOR = (0x40, 0x40, 0x40)
    ACCENT_COLOR = (0x20, 0x20, 0x20)

    surface = None

    close_btn = None

    win_rect = (0, 0, 0, 0)

    dismissable = True
    closed = False

    def __init__(self, *args, **kwargs):
        super(DialogBase, self).__init__(*args, **kwargs)
        self.calc_rect()
        self.surface = pygame.Surface((self.win_rect[2], self.win_rect[3]))

    def calc_rect(self):
        self.win_rect = (
            self.WIN_PAD, 
            self.WIN_PAD, 
            self.resolution[0]-self.WIN_PAD*2, 
            self.resolution[1]-self.WIN_PAD*2
        )

    def win_width(self):
        return self.win_rect[2]

    def win_height(self):
        return self.win_rect[3]

    def in_window(self, loc):
        if loc_inside(loc, self.win_rect):
            return True
        return False

    def in_titlebar(self, loc):
        rect = (self.win_rect[0], self.win_rect[1], self.win_width(), self.TITLEBAR_HEIGHT)
        if loc_inside(loc, rect):
            return True
        return False

    def in_closebtn(self, loc):
        if not self.dismissable:
            return False

        CLOSEBTN_WIDTH = self.TITLEBAR_HEIGHT

        rect = (
            self.win_rect[0]+self.win_width()-CLOSEBTN_WIDTH,
            self.win_rect[1],
            CLOSEBTN_WIDTH,
            CLOSEBTN_WIDTH
        )

        if loc_inside(loc, rect):
            return True
        return False

    def loc_conv_window(self, loc):
        return (loc[0]-self.win_rect[0], loc[1]-self.win_rect[1])

    def draw_components(self, screen):
        screen.fill(self.BG_COLOR)

        # Draw title bar
        titlebar_rect = (0, 0, self.win_width(), self.TITLEBAR_HEIGHT)
        pygame.draw.rect(screen, self.ACCENT_COLOR, titlebar_rect)

        # Draw title text
        title = render_text(
            self.title_text, 
            size=20, 
            font='./assets/HelveticaNeue.ttf', 
            bg=None
        )
        title_pos = align(title.get_rect(), titlebar_rect, horizontal=ALIGN_LEFT, hpad=15)
        screen.blit(title, title_pos)

        # Draw close button
        if self.dismissable:
            self.draw_closebtn(screen)
            titlebar_rect = (0, 0, self.win_width()-self.TITLEBAR_HEIGHT, self.TITLEBAR_HEIGHT)

        # Draw dialog count
        d_count = self.controller.dialog_count()
        if d_count > 1:
            d_count_label = render_text(
                f'({d_count})', 
                size=16, 
                font='./assets/HelveticaNeue.ttf', 
                fg=(128, 128, 128), 
                bg=None
            )
            d_count_pos = align(d_count_label.get_rect(), titlebar_rect, horizontal=ALIGN_RIGHT, hpad=-10)
            screen.blit(d_count_label, d_count_pos)

        # Title bar shadow
        pygame.draw.line(
            screen, 
            (0x16, 0x16, 0x16), 
            (0, self.TITLEBAR_HEIGHT), 
            (self.win_width(), self.TITLEBAR_HEIGHT)
        )

    def draw_closebtn(self, screen):
        if self.close_btn is None:
            self.close_btn = DialogCloseButton(self.TITLEBAR_HEIGHT, 4, click=self.close)

        loc = (self.win_width()-self.TITLEBAR_HEIGHT, 1)
        self.close_btn.render(screen, loc)

    def draw_dialog(self, screen):
        pass

    def internal_render(self, screen):
        # Draw dialog components
        self.draw_components(screen)

        # Draw dialog contents
        self.draw_dialog(screen)

    def render(self, screen):
        self.internal_render(self.surface)

        # Draw shadow
        pygame.draw.rect(screen, (0, 0, 0, 192), (
            self.win_rect[0]+1,
            self.win_rect[1]+1,
            self.win_rect[2]+1,
            self.win_rect[3]+1
        ))

        # Draw window
        screen.blit(self.surface, self.win_rect)

    def register_event(self, event, loc, *args, **kwargs):
        # Clicks outside window dismisses window
        # if self.dismissable and event == 'click' and not self.in_window(loc):
        #     self.closed = True
        #     return

        # Handle excessive lift events from 'click'-based callbacks
        if self.closed is True and event == 'lift':
            self.close()
            return

        # Handle close button
        if self.close_btn is not None and event in ('press', 'lift', 'drag'):
            getattr(self.close_btn, event)(self.loc_conv_window(loc), *args, **kwargs)


    def close(self):
        self.controller.delete_dialog(self)
