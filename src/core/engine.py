# Import
from settings import *

# Engine class
class Engine:
	# Constructor
	def __init__(self, app):
		self.app = app

	# Update function
	def update(self):
		pass

	# Draw function
	def draw(self):
		# Begin drawing
		ray.begin_drawing()
		ray.clear_background(ray.BLACK)

		# End drawing
		ray.end_drawing()
