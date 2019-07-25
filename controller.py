import pygame

from views.navbar import Navbar
from views.dashboard import DashboardView
from views.dialog.alert import AlertDialog

from constants import *

class FxSdrController(object):

	RootView = None
	ViewHistory = []
	NavBar = None
	Dialog = []

	screen_scale = None
	navbar_height = None

	s_content = None
	s_navbar = None
	s_dialog = None

	def __init__(self, app):
		self.app = app

		self.init_surfaces()

		self.init_navbar()
		self.init_rootview(DashboardView)

	# ---- Initialization methods ----

	def init_navbar(self):
		self.Navbar = Navbar(self.navbar_resolution(), self)		

	def init_rootview(self, root_view):
		self.RootView = root_view(self.content_resolution(), self)

	def init_surfaces(self):
		self.s_content = pygame.Surface(self.content_resolution())
		self.s_navbar = pygame.Surface(self.navbar_resolution())
		self.s_dialog = pygame.Surface(self.app.resolution, pygame.SRCALPHA)

	# ---- Updater methods ----

	def update_navbar(self):
		title = 'FxSDR'
		if not self.is_root():
			title = self.current().title()

			if self.get_screen_scale() == SCREEN_SMALL:
				self.Navbar.back_btn.set_text('Back')
			else:
				if len(self.ViewHistory) >= 2:
					self.Navbar.back_btn.set_text(self.ViewHistory[-2].title())
				elif len(self.ViewHistory) == 1:
					self.Navbar.back_btn.set_text(self.RootView.title())
				else:
					self.Navbar.back_btn.set_text('Back')

		self.Navbar.title_text = title

	# ---- View changing methods ----

	def go_root(self):
		if self.is_root():
			return False

		self.ViewHistory = []
		self.update_navbar()
		return True

	def segue(self, next_view):
		view = next_view(self.content_resolution(), self)
		self.ViewHistory.append(view)
		self.update_navbar()
		return True

	def back(self):
		if self.is_root():
			return False

		del self.ViewHistory[-1]
		self.update_navbar()

	def init_dialog(self, dialog_class):
		return dialog_class(self.app.resolution, self)

	def show_dialog(self, dialog):
		self.Dialog.append(dialog)

	def show_alert(self):
		alert = self.init_dialog(AlertDialog)



		self.show_dialog(alert)


	# ---- Getter methods ----

	def get_screen_scale(self):
		if self.screen_scale is None:
			if self.app.resolution[1] < 320:
				self.screen_scale = SCREEN_SMALL
			elif self.app.resolution[1] < 480:
				self.screen_scale = SCREEN_MEDIUM
			else:
				self.screen_scale = SCREEN_LARGE

		return self.screen_scale

	def get_navbar_height(self):
		if self.navbar_height is None:
			self.navbar_height = 48 # Default
			if self.get_screen_scale() == SCREEN_SMALL:
				self.navbar_height = 36
			elif self.get_screen_scale() == SCREEN_MEDIUM:
				self.navbar_height = 48
			elif self.get_screen_scale() == SCREEN_LARGE:
				self.navbar_height = 56

		return self.navbar_height

	def navbar_resolution(self):
		return (self.app.resolution[0], self.get_navbar_height())

	def content_resolution(self):
		return (self.app.resolution[0], self.app.resolution[1] - self.get_navbar_height())

	def content_rel(self, loc):
		return (loc[0], loc[1] - self.get_navbar_height())

	def in_navbar(self, loc):
		return (loc[1] <= self.get_navbar_height())

	def in_content(self, loc):
		return (loc[1] > self.get_navbar_height())

	def is_view(self, view_class):
		return self.current().__class__ is view_class

	def is_root(self):
		if len(self.ViewHistory) <= 0:
			return True
		return False

	def current(self):
		if self.is_root():
			return self.RootView
		else:
			return self.ViewHistory[-1]

	def is_dialog_present(self):
		if len(self.Dialog) > 0:
			return True
		return False

	def dialog(self):
		if self.is_dialog_present():
			return self.Dialog[-1]
		return False

	# ---- Event listeners ----

	def m_press(self, loc):
		if self.in_content(loc):
			self.current().press(self.content_rel(loc))
		else:
			self.Navbar.press(loc)

	def m_drag(self, loc):
		if self.in_content(loc):
			self.current().drag(self.content_rel(loc))
		else:
			self.Navbar.drag(loc)

	def m_click(self, loc):
		if self.in_content(loc):
			self.current().click(self.content_rel(loc))
		else:
			self.Navbar.click(loc)

	def m_lift(self, loc):
		self.current().lift(self.content_rel(loc))
		self.Navbar.lift(loc)

	# ---- Rendering methods ----

	def render_current(self, screen):
		if not self.is_dialog_present():
			self.current().render(self.s_content)
			self.Navbar.render(self.s_navbar)

			seq = (
				(self.s_content, (0, self.get_navbar_height())),
				(self.s_navbar, (0, 0))
			)
		else:
			self.s_dialog.fill((0, 0, 0, 128))
			self.s_dialog.set_alpha(255)
			self.dialog().render(self.s_dialog)

			seq = (
				(self.s_content, (0, self.get_navbar_height())),
				(self.s_navbar, (0, 0)),
				(self.s_dialog, (0, 0))
			)

		screen.blits(blit_sequence=seq)



