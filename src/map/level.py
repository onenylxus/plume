# Import
from common import *
from map.segment import Segment

# Level class
class Level:
  # Constructor
  def __init__(self, engine, settings, segments):
    # Define properties
    self.engine = engine
    self.settings = settings
    self.segments = [Segment(start, end) for (start, end) in segments]
