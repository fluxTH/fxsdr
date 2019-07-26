import os
import pygame
from time import time, sleep

from controller import FxSdrController

class FxSdrApp():

    DEBUG = False
    SETTINGS = {
        'CLICK_DEBOUNCE': 0.4
    }

    # resolution = (720, 480)
    resolution = (480, 320)
    # resolution = (320, 240)

    clock = None
    controller = None
    screen = None
    # surface = None

    mouse_hold = False
    mouse_downpos = None
    mouse_lastclick = 0

    exited = False

    def __init__(self, settings={}, debug=False):
        self.DEBUG = debug
        self.SETTINGS = {**self.SETTINGS, **settings}
        self.init_driver()
        self.init_screen()
        self.init_clock()
        self.init_controller()

    def init_driver(self):
        # Init pygame SDL
        if not self.DEBUG:
            # Initialize pygame and SDL to use the PiTFT display and touchscreen.
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')
            os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
            os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')
        pygame.display.init()
        pygame.display.set_caption('arm64 emulator (ARMv8-A)')
        pygame.font.init()

        # Init Cursor
        if self.DEBUG:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_visible(False)

    def init_screen(self):
        # Init display
        if self.DEBUG:
            self.screen = pygame.display.set_mode(self.resolution)
        else:
            self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)

        # self.screen.fill((0xcd, 0xd2, 0xdd))
        # pygame.display.update()

        # self.surface = pygame.Surface(self.resolution)

    def init_clock(self):
        self.clock = pygame.time.Clock()

    def init_controller(self):
        self.controller = FxSdrController(self)

    def run(self):
        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.exited = True
        finally:
            print('Exited')

    def main_loop(self):
        while not self.exited:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.exited = True
                    continue

                if event.type is pygame.MOUSEBUTTONDOWN \
                    and time() - self.mouse_lastclick > self.SETTINGS['CLICK_DEBOUNCE']:

                    self.mouse_hold = True
                    self.mouse_downpos = event.pos

                    self.controller.m_press(event.pos)

                elif event.type is pygame.MOUSEBUTTONUP:
                    if self.mouse_hold is True:
                        if self.mouse_downpos == event.pos:
                            self.controller.m_click(event.pos)
                        
                        self.controller.m_lift(event.pos)

                        self.mouse_lastclick = time()
                    self.mouse_hold = False

                else:
                    if self.mouse_hold and event.type is pygame.MOUSEMOTION:
                        self.controller.m_drag(event.pos)

            self.controller.render_current(self.screen)
            pygame.display.update()

            self.clock.tick(20)


