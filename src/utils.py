# Import
from common import *

# Cross function for two-dimensional space
def cross_2d(start, end):
  return start.x * end.y - start.y * end.x

# Check start vector is in front of end vector
def is_front(start, end):
  return start.x * end.y < start.y * end.x
