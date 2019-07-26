class ViewBase(object):
    """Base class for simple UI view which represents all the elements drawn
    on the screen.  Subclasses should override the render, and click functions.
    """
    resolution = (0, 0)
    controller = None

    title_text = ''

    def __init__(self, res, controller):
        self.resolution = res
        self.controller = controller

    def set_title(self, title):
        self.title_text = title

    def render(self, screen):
        pass

    def register_event(self, event, *args, **kwargs):
        pass

    def press(self, loc):
        self.register_event('press', loc)

    def drag(self, loc):
        self.register_event('drag', loc)

    def click(self, loc):
        self.register_event('click', loc)

    def lift(self, loc):
        self.register_event('lift', loc)

class ContentBase(ViewBase):
    BG_COLOR = (0x24, 0x24, 0x24)

    def title(self):
        return 'View'