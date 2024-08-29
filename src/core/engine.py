# Import
from common import *
from core.renderer import Renderer
from map.level import Level
from resources.levels.test import segments as test_segments

# Engine class
class Engine:
	# Constructor
	def __init__(self, app):
		self.app = app
		self.level = Level(self, test_segments)
		self.renderer = Renderer(self)

	# Update function
	def update(self):
		self.renderer.update()

	# Draw function
	def draw(self):
		# Begin drawing
		ray.begin_drawing()
		ray.clear_background(BG_COLOR)

		self.renderer.draw()

		# End drawing
		ray.end_drawing()
