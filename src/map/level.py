# Import
from common import *
from map.segment import Segment

# Level class
class Level:
  # Constructor
  def __init__(self, engine, segments):
    # Define properties
    self.engine = engine
    self.segments: list[Segment] = [Segment(start, end) for (start, end) in segments]
