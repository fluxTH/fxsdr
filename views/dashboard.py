from ui.utils import render_text
from views import ContentBase


class DashboardView(ContentBase):
    def title(self):
        return 'Dashboard'

    def render(self, screen):
        screen.fill(self.BG_COLOR)
        text = render_text('Dashboard pls', size=24, font='./assets/HelveticaNeueBold.ttf', bg=None)
        screen.blit(text, (0,0))

    def click(self, loc):
        self.controller.segue(Test2)

class Test2(ContentBase):
    def title(self):
        return 'Test Page 2'

    def render(self, screen):
        screen.fill(self.BG_COLOR)
        text = render_text('test 2', size=24, font='./assets/HelveticaNeueBold.ttf', bg=None)
        screen.blit(text, (0,0))

    def click(self, loc):
        self.controller.segue(Test3)

class Test3(ContentBase):

    def title(self):
        return 'Page 3 mofos'

    def render(self, screen):
        screen.fill(self.BG_COLOR)
        text = render_text('three!', size=24, font='./assets/HelveticaNeueBold.ttf', bg=None)
        screen.blit(text, (0,0))

    def click(self, loc):
        self.controller.segue(Test4)

class Test4(ContentBase):

    def title(self):
        return 'Test Page 4'

    def render(self, screen):
        screen.fill(self.BG_COLOR)
        text = render_text('四 กขค page', size=24, font='./assets/HelveticaNeueBold.ttf', bg=None)
        screen.blit(text, (0,0))