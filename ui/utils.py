import pygame

from constants import *


def align(child, parent, horizontal=ALIGN_CENTER, vertical=ALIGN_CENTER,
	hpad=0, vpad=0):
	"""Return tuple of x, y coordinates to render the provided child rect 
	aligned inside the parent rect using the provided horizontal and vertical
	alignment.  Each alignment value can be ALIGN_LEFT, ALIGNT_TOP, ALIGN_CENTER,
	ALIGN_RIGHT, or ALIGN_BOTTOM.  Can also specify optional horizontal padding
	(hpad) and vertical padding (vpad).
	"""
	cx, cy, cwidth, cheight = child
	px, py, pwidth, pheight = parent
	return (px+(horizontal*pwidth-horizontal*cwidth)+hpad,
			py+(vertical*pheight-vertical*cheight)+vpad)

font_cache = {}
def get_font(size, font=None):
	"""Get font of the specified size.  Will cache fonts internally for faster
	repeated access to them.
	"""
	if size not in font_cache:
		font_cache[size] = pygame.font.Font(font, size)
	return font_cache[size]

def render_text(text, size=33, font='./assets/HelveticaNeue.ttf', fg=(255, 255, 255), bg=(0, 0, 0)):
	"""Render the provided text to a surface which is returned."""
	if bg is not None:
		# Optimized case when the background is known.
		return get_font(size, font).render(text, True, fg, bg)
	else:
		# Less optimized case with transparent background.
		return get_font(size, font).render(text, True, fg)

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def loc_inside(loc, rect):
	if loc is None or rect is None:
		return False
		
	x, y, width, height = rect
	mx, my = loc
	if mx >= x and mx <= (x + width) and my >= y and my <= (y + height):
		return True
	return False



