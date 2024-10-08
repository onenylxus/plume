# Import
from glm import normalize, vec2
from math import ceil
import pyray as ray
import random

# Window resolution
WINDOW_RESOLUTION = WINDOW_WIDTH, WINDOW_HEIGHT = 640, 360

# Map display
MAP_OFFSET = 20
DISPLAY_X_MIN, DISPLAY_X_MAX = MAP_OFFSET, WINDOW_WIDTH - MAP_OFFSET
DISPLAY_Y_MIN, DISPLAY_Y_MAX = MAP_OFFSET, WINDOW_HEIGHT - MAP_OFFSET

# Colors
BG_COLOR = ray.BLACK
VERTEX_COLOR = ray.WHITE
SOURCE_COLOR = ray.DARKGRAY
SEGMENT_COLOR = ray.YELLOW
NORMAL_COLOR = ray.ORANGE
PLAYER_COLOR = ray.GREEN

# Values
EPS = 1e-4
INF = float('inf')
