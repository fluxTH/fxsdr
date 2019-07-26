from ui.utils import loc_inside

class UIComponentBase():
    surface = None
    location = (0, 0)

    def get_rect(self, pad=True):
        # Returns externally used rect
        # For internal rect, use self.surface.get_rect()
        return self.surface.get_rect(topleft=self.location)

    def render(self, screen, loc):
        self.location = loc

class UIPressable(UIComponentBase):

    click_func = None

    pressed = False
    pressed_at = None

    def press(self, loc):
        if loc_inside(loc, self.get_rect()):
            self.pressed = True
            self.pressed_at = loc

    def drag(self, loc):
        if loc_inside(loc, self.get_rect()):
            if loc_inside(self.pressed_at, self.get_rect()):
                self.pressed = True
        else:
            self.pressed = False

    def lift(self, loc):
        if self.pressed is True:
            if self.click_func is not None:
                self.click_func()

        self.pressed = False
        self.pressed_at = None

class UIException(Exception):
    pass