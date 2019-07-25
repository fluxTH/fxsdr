from ui.utils import render_text
from views import ContentBase

class SettingsView(ContentBase):
	def title(self):
		return 'Settings'

	def render(self, screen):
		screen.fill(self.BG_COLOR)
		text = render_text('SETTINGS', size=16, font='./assets/HelveticaNeue.ttf', bg=None)
		screen.blit(text, (0,0))

class AboutView(ContentBase):
	def title(self):
		return 'About'

	def render(self, screen):
		screen.fill(self.BG_COLOR)
		text = render_text('v1', size=16, font='./assets/HelveticaNeue.ttf', bg=None)
		screen.blit(text, (0,0))