import pygame

from ui.utils import render_text, align
from views import ViewBase

from constants import *


class DialogBase(ViewBase):
	WIN_PAD = 30
	TITLEBAR_HEIGHT = 40

	BG_COLOR = (0x40, 0x40, 0x40)
	ACCENT_COLOR = (0x20, 0x20, 0x20)

	surface = None
	win_rect = (0, 0, 0, 0)

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

	def draw_components(self, screen):
		screen.fill(self.BG_COLOR)

		# Draw title bar
		titlebar_rect = (0, 0, self.win_width(), self.TITLEBAR_HEIGHT)
		pygame.draw.rect(screen, self.ACCENT_COLOR, titlebar_rect)

		# Draw title text
		title = render_text(
			'Alert', 
			size=20, 
			font='./assets/HelveticaNeue.ttf', 
			bg=None
		)
		title_pos = align(title.get_rect(), titlebar_rect, horizontal=ALIGN_LEFT, hpad=15)
		screen.blit(title, title_pos)

		# Draw close button
		if True: # TODO
			self.draw_closebtn(screen)
			titlebar_rect = (0, 0, self.win_width()-self.TITLEBAR_HEIGHT, self.TITLEBAR_HEIGHT)

		# Draw dialog count
		d_count = render_text(
			'(2)', 
			size=16, 
			font='./assets/HelveticaNeue.ttf', 
			fg=(128, 128, 128), 
			bg=None
		)
		d_count_pos = align(d_count.get_rect(), titlebar_rect, horizontal=ALIGN_RIGHT, hpad=-10)
		screen.blit(d_count, d_count_pos)

		# Title bar shadow
		pygame.draw.line(
			screen, 
			(0x16, 0x16, 0x16), 
			(0, self.TITLEBAR_HEIGHT), 
			(self.win_width(), self.TITLEBAR_HEIGHT)
		)

	def draw_dialog(self, screen):
		pass

	def draw_closebtn(self, screen):
		close_rect = (
			self.win_width()-self.TITLEBAR_HEIGHT,
			1, 
			self.TITLEBAR_HEIGHT, 
			self.TITLEBAR_HEIGHT-1
		)

		# Draw button
		pygame.draw.rect(screen, (150,0,0), close_rect)

		x_size = self.TITLEBAR_HEIGHT / 2
		x_xleft = close_rect[0]+x_size/2
		x_xright = close_rect[0]+close_rect[2]-x_size/2
		x_ytop = close_rect[1]+x_size/2
		x_ybottom = close_rect[1]+close_rect[3]-x_size/2

		# Draw X
		pygame.draw.aaline(screen, (255, 255, 255), (x_xleft, x_ytop), (x_xright, x_ybottom), 2)
		pygame.draw.aaline(screen, (255, 255, 255), (x_xright, x_ytop), (x_xleft, x_ybottom), 2)

	def render(self, screen):		
		# Draw dialog components
		self.draw_components(self.surface)
		self.draw_dialog(self.surface)

		# Draw shadow
		pygame.draw.rect(screen, (0, 0, 0, 192), (
			self.win_rect[0]+1,
			self.win_rect[1]+1,
			self.win_rect[2]+1,
			self.win_rect[3]+1
		))

		# Draw window
		screen.blit(self.surface, self.win_rect)
