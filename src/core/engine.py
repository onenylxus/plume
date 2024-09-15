# Import
from common import *
from core.renderer import Renderer
from map.bsp import BSPBuilder, BSPTraverser
from map.level import Level
from resources.levels.test import settings as test_settings, segments as test_segments

# Engine class
class Engine:
	# Constructor
	def __init__(self, app):
		# Define properties
		self.app = app
		self.level = Level(self, test_settings, test_segments)
		self.bsp_builder = BSPBuilder(self)
		self.bsp_traverser = BSPTraverser(self)
		self.renderer = Renderer(self)

	# Update function
	def update(self):
		self.bsp_traverser.update()

	# Draw function
	def draw(self):
		# Begin drawing
		ray.begin_drawing()
		ray.clear_background(BG_COLOR)

		self.renderer.draw()

		# End drawing
		ray.end_drawing()
