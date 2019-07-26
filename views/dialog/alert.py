import pygame

from ui.dialog import DialogButtonRowFooter, DialogTextBody
from ui.input import Button, DangerButton

from views.dialog import DialogBase

class AlertDialog(DialogBase):

    FOOTER_HEIGHT = 60

    footer = None

    def __init__(self, *args, **kwargs):
        super(AlertDialog, self).__init__(*args, **kwargs)
        self.FOOTER_HEIGHT = self.controller.get_dialog_footer()
        self.footer = DialogButtonRowFooter(self)
        self.body = DialogTextBody((
            self.content_width(), 
            self.content_height()-self.FOOTER_HEIGHT
        ))


        self.init_footer()
        self.init_body()

    def init_footer(self):
        pass

    def init_body(self):
        pass

    def draw_dialog(self, screen):
        self.footer.render(screen, (self.content_rect[0], self.content_rect[3]-self.FOOTER_HEIGHT))
        self.body.render(screen, (0, 0))

    def register_event(self, event, loc, *args, **kwargs):
        super(AlertDialog, self).register_event(event, loc, *args, **kwargs)

        if event in ('press', 'drag', 'lift'):
            getattr(self.footer, event)(self.loc_conv_content(loc), *args, **kwargs)


class ExitConfirmDialog(AlertDialog):
    def init_footer(self):
        cancel = Button('Cancel', self.close)
        self.footer.add_button(cancel)

        exit = DangerButton('Exit', self.controller.app.exit)
        self.footer.add_button(exit)

    def init_body(self):
        self.dismissable = False
        self.set_title('Confirmation')

        self.body.BG_COLOR = self.BG_COLOR
        self.body.set_body_text(
            'Analyzer and audio will stop if you exit.\n' + \
            'Are you sure you want to continue?'
        )
