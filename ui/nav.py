import pygame
from ui.utils import fill, render_text, loc_inside

class NavBase():
	TEXT_COLOR = (0xff, 0xff, 0xff)
	LINK_COLOR = (0xe6, 0x94, 0x10)
	LINK_HOLD_COLOR = (0x75, 0x48, 0)

class NavButton(NavBase):

	size = 16
	btn_text = ''

	surface = None
	location = (0, 0)

	pressed = False
	pressed_at = None
	surface_pressed = False

	def __init__(self, text, size=16, click=None):
		self.click_func = click
		self.size = size
		self.set_text(text)

	def set_text(self, text):
		self.btn_text = text
		self.internal_render()

	def internal_render(self):
		color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
		self.surface = render_text(self.btn_text, size=self.size, fg=color, bg=None)
		self.surface_pressed = self.pressed

	def get_rect(self):
		return self.surface.get_rect(topleft=self.location)

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

	def render(self, screen, loc):
		if not self.pressed == self.surface_pressed:
			self.internal_render()

		self.location = loc
		screen.blit(self.surface.convert_alpha(), loc)

class NavBackButton(NavButton):

	back_icon = None
	
	def __init__(self, text, size=16, click=None):

		self.click_func = click
		self.size = size

		self.back_icon = pygame.image.load('./assets/back.png').convert_alpha()
		self.back_icon = pygame.transform.scale(self.back_icon, (25, 25))

		self.set_text(text)

	def internal_render(self):
		color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
		text = render_text(self.btn_text, size=self.size, fg=color, bg=None)
		
		fill(self.back_icon, color)

		_, _, tw, th = text.get_rect()
		_, _, iw, ih = self.back_icon.get_rect()

		self.surface = pygame.Surface((tw+iw, max(th, ih)), pygame.SRCALPHA, 32)
		self.surface_pressed = self.pressed

		self.surface.blits(blit_sequence=(
			(self.back_icon, (0, 0)),
			(text, (iw, abs(ih-th)/2))
		))

class NavFreqButton(NavButton):

	def __init__(self, text, size=16, click=None):

		self.click_func = click
		self.size = size

		self.set_text(text)

	def internal_render(self):
		if not self.btn_text == 'OFF':
			color = self.LINK_HOLD_COLOR if self.pressed else self.LINK_COLOR
		else:
			color = (150, 0, 0) if self.pressed else (255, 0, 0)

		self.surface = render_text(self.btn_text, size=self.size, fg=color, bg=None)
		self.surface_pressed = self.pressed

class NavText(NavBase):
	pass

class NavTitle(NavText):
	pass