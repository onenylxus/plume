# Import
from common import *
from map.segment import Segment

# Renderer class
class Renderer:
	# Constructor
	def __init__(self, engine):
		# Define properties
		self.engine = engine
		self.segments = []
		self.x_min, self.y_min, self.x_max, self.y_max = INF, INF, -INF, -INF
		self.coords = []

		# Update call on initialize
		self.update()

	# Get segment pairs
	def get_segment_pairs(self):
		# Check current level exists
		if self.engine.level is None:
			return []

		# Get pairs from current level
		return [segment.get_pair() for segment in self.engine.level.segments]

	# Get level boundaries
	def get_bounds(self):
		# Reset boundaries
		x_min, y_min, x_max, y_max = INF, INF, -INF, -INF

		# Compare through segments
		for start, end in self.segments:
			x_min = start.x if start.x < x_min else end.x if end.x < x_min else x_min
			y_min = start.y if start.y < y_min else end.y if end.y < y_min else y_min
			x_max = start.x if start.x > x_max else end.x if end.x > x_max else x_max
			y_max = start.y if start.y > y_max else end.y if end.y > y_max else y_max

		# Return
		return x_min, y_min, x_max, y_max

	# Remap x-axis value
	def remap_x(self, x):
		return (x - self.x_min) * (DISPLAY_X_MAX - DISPLAY_X_MIN) / (self.x_max - self.x_min) + DISPLAY_X_MIN

	# Remap y-axis value
	def remap_y(self, y):
		return (y - self.y_min) * (DISPLAY_Y_MAX - DISPLAY_Y_MIN) / (self.y_max - self.y_min) + DISPLAY_Y_MIN

	# Remap vector
	def remap_vector(self, vec):
		return vec2(self.remap_x(vec.x), self.remap_y(vec.y))

	# Get coordinates
	def get_coords(self):
		return [(self.remap_vector(start), self.remap_vector(end)) for start, end in self.segments]

	# Update function
	def update(self):
		# Update level data
		self.segments = self.get_segment_pairs()
		self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds()
		self.coords = self.get_coords()

	# Draw segment
	def draw_segment(self, start, end):
		segment = Segment(start, end)
		n_start = (start + end) / 2
		n_end = n_start + segment.get_normal() * 4

		ray.draw_line_v((start.x, start.y), (end.x, end.y), SEGMENT_COLOR)
		ray.draw_line_v((n_start.x, n_start.y), (n_end.x, n_end.y), NORMAL_COLOR)
		ray.draw_circle_v((start.x, start.y), 3, VERTEX_COLOR)

	# Draw function
	def draw(self):
		# Draw coordinates
		for start, end in self.coords:
			self.draw_segment(start, end)

