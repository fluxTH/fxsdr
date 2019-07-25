class ViewBase(object):
	"""Base class for simple UI view which represents all the elements drawn
	on the screen.  Subclasses should override the render, and click functions.
	"""
	resolution = (0, 0)
	controller = None

	def __init__(self, res, controller):
		self.resolution = res
		self.controller = controller

	def render(self, screen):
		pass

	def press(self, location):
		pass

	def drag(self, location):
		pass

	def click(self, location):
		pass

	def lift(self, location):
		pass

class ContentBase(ViewBase):
	BG_COLOR = (0x24, 0x24, 0x24)

	def title(self):
		return 'View'