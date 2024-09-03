# Import
from common import *
from map.segment import Segment

# Renderer class
class Renderer:
	# Constructor
	def __init__(self, engine):
		# Define properties
		self.engine = engine
		self.source = []
		self.segments = []
		self.x_min, self.y_min, self.x_max, self.y_max = INF, INF, -INF, -INF
		self.coords = []

		# Temporary
		self.counter = 0.0

		# Initialize
		self.fetch()

	# Fetch data from engine
	def fetch(self):
		# Get segment pairs from level and update limits
		if self.engine.level is not None:
			self.source = [segment.get_pair() for segment in self.engine.level.segments]
			self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds()
			self.coords = self.get_coords()

		# Get segments from BSP builder
		if self.engine.bsp_builder is not None:
			self.segments = [segment.get_pair() for segment in self.engine.bsp_builder.segments]
			self.counter = 0.0

	# Get level boundaries
	def get_bounds(self):
		# Reset boundaries
		x_min, y_min, x_max, y_max = INF, INF, -INF, -INF

		# Compare through segments
		for start, end in self.source:
			x_min = start.x if start.x < x_min else end.x if end.x < x_min else x_min
			y_min = start.y if start.y < y_min else end.y if end.y < y_min else y_min
			x_max = start.x if start.x > x_max else end.x if end.x > x_max else x_max
			y_max = start.y if start.y > y_max else end.y if end.y > y_max else y_max

		# Return
		return x_min, y_min, x_max, y_max

	# Remap x-axis value
	def remap_x(self, x):
		return (x - self.x_min) * min(DISPLAY_X_MAX - DISPLAY_X_MIN, DISPLAY_Y_MAX - DISPLAY_Y_MIN) / (self.x_max - self.x_min) + DISPLAY_X_MIN

	# Remap y-axis value
	def remap_y(self, y):
		return (y - self.y_min) * min(DISPLAY_X_MAX - DISPLAY_X_MIN, DISPLAY_Y_MAX - DISPLAY_Y_MIN) / (self.y_max - self.y_min) + DISPLAY_Y_MIN

	# Remap vector
	def remap_vector(self, vec):
		return vec2(self.remap_x(vec.x), self.remap_y(vec.y))

	# Get coordinates
	def get_coords(self):
		return [(self.remap_vector(start), self.remap_vector(end)) for start, end in self.source]

	# Draw normal from segment
	def draw_normal(self, segment):
		normal_start = (segment.start + segment.end) / 2
		normal_end = normal_start + segment.get_normal() * 10

		ray.draw_line_v((normal_start.x, normal_start.y), (normal_end.x, normal_end.y), NORMAL_COLOR)

	# Draw source segment
	def draw_source(self):
		for start, end in self.coords:
			ray.draw_line_v((start.x, start.y), (end.x, end.y), SOURCE_COLOR)
			ray.draw_circle_v((start.x, start.y), 3, VERTEX_COLOR)

	# Draw visible segments
	def draw_segments(self):
		if self.engine.bsp_traverser is None:
			return

		ids = self.engine.bsp_traverser.ids
		for id in ids[:int(self.counter) % (len(ids) + 1)]:
			start, end = self.segments[id]
			start = self.remap_vector(start)
			end = self.remap_vector(end)

			ray.draw_line_v((start.x, start.y), (end.x, end.y), SEGMENT_COLOR)
			self.draw_normal(Segment(start, end))
			ray.draw_circle_v((start.x, start.y), 3, VERTEX_COLOR)
			ray.draw_circle_v((end.x, end.y), 3, VERTEX_COLOR)

	# Draw player
	def draw_player(self):
		if self.engine.bsp_traverser is None:
			return

		x, y = self.remap_vector(self.engine.bsp_traverser.pos)

		ray.draw_circle_v((x, y), 5, PLAYER_COLOR)

	# Draw function
	def draw(self):
		self.draw_source()
		self.draw_segments()
		self.draw_player()

		# Temporary
		self.counter += EPS * 5

