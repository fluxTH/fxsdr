import pygame


class Grid(object):
	def __init__(self, width, height, cols, rows):
		"""Create grid of buttons with the provided total width and height in
		pixels and subdivided into cols x rows equally sized buttons.
		"""
		self.col_size = width / cols
		self.row_size = height / rows
		self.objects = []

	def add(self, obj, col, row, text, rowspan=1, colspan=1):
		"""Add a Button to the grid at the specified row and col position in
		the grid.  Row and col are 0-based indexes.  Buttons can span multiple
		rows and columns by providing optional rowspan and colspan parameters.
		Any other keyword arguments are passed to the Button constructor.
		"""
		x = col*self.col_size
		y = row*self.row_size
		width = colspan*self.col_size
		height = rowspan*self.row_size
		self.objects.append(obj)

	def render(self, screen):
		"""Render buttons on the provided surface."""
		# Render buttons.
		for obj in self.objects:
			obj.render(screen)

	def press(self, location):
		pass

	def drag(self, location):
		pass

	def click(self, location):
		"""Handle click events at the provided location tuple (x, y) for all the
		buttons.
		"""
		for obj in self.objects:
			obj.click(location)

	def lift(self, location):
		pass
