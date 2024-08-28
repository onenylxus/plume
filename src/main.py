# Import
from core.engine import Engine
from settings import *

# Application class
class App:
	# Constructor
	def __init__(self):
		self.engine = Engine(app = self)
		self.delta = 0.0

		# Initialize window
		ray.init_window(WIDTH, HEIGHT, 'Plume Engine')

	# Run function
	def run(self):
		# Event loop
		while not ray.window_should_close():
			self.delta = ray.get_frame_time()
			self.engine.update()
			self.engine.draw()

		# Close window
		ray.close_window()

# Main function
if __name__ == '__main__':
	app = App()
	app.run()
