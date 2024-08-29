# Import
from common import *

# Segment class
class Segment:
	# Constructor
  def __init__(self, start, end):
    self.start = vec2(start)
    self.end = vec2(end)

	# Get pair
  def get_pair(self):
    return self.start, self.end

	# Get vector
  # Segment vector is a vector from start vertex to end vertex
  def get_vector(self):
    return self.end - self.start

	# Get normal
  # Normal is an unit vector perpendicular and at the right side of the segment vector
  def get_normal(self):
    vec = self.get_vector()
    perp = vec2(-vec.y, vec.x)
    return normalize(perp)
