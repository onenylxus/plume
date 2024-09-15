# Import
from common import *
from copy import copy
import multiprocessing as mp
from utils import cross_2d, is_front

# BSP node class
class BSPNode:
	# Constructor
	def __init__(self):
		# Define properties
		self.front = None
		self.back = None
		self.splitter = None
		self.id = None

# BSP builder class
class BSPBuilder:
	# Constructor
	def __init__(self, engine):
		# Define properties
		self.engine = engine
		self.source = []
		self.segments = []
		self.root = BSPNode()
		self.id = 0
		self.front_count, self.back_count, self.split_count = 0, 0, 0

		# Initialize
		self.fetch()

	# Reset function
	def reset(self):
		self.segments = []
		self.root = BSPNode()
		self.id = 0
		self.front_count, self.back_count, self.split_count = 0, 0, 0

	# Fetch data from engine
	def fetch(self):
		# Get source segments
		if self.engine.level is not None:
			self.source = self.engine.level.segments

			# Build tree with best seed
			seed = self.engine.level.settings['seed']
			if seed < 0:
				seed = self.find_best_seed_mp()
			random.seed(seed)
			random.shuffle(self.source)
			self.reset()
			self.build_tree(self.root, self.source)

			# Print partitioning statistics
			print(f"[BSPBuilder] Front segments: {self.front_count}")
			print(f"[BSPBuilder] Back segments: {self.back_count}")
			print(f"[BSPBuilder] Splits: {self.split_count}")

	# Find best seed
	def find_best_seed(self, start_seed = 0, end_seed = 10000, weight = 3, index = 0, results = {}):
		# Define variables
		best_seed, best_score = -1, INF

		# Iterate through seeds
		for seed in range(start_seed, end_seed):
			source = self.source.copy()
			root = BSPNode()

			# Build tree virtually
			random.seed(seed)
			random.shuffle(source)
			self.reset()
			self.build_tree(root, source)

			# Calculate score
			score = abs(self.back_count - self.front_count) + weight * self.split_count
			if score < best_score:
				best_seed, best_score = seed, score

		# Print result
		print(f"[BSPBuilder] Best seed is #{best_seed} with score {best_score}")

		# Return
		results[index] = (best_seed, best_score)
		return best_seed

	# Find best seed with multiprocessing
	def find_best_seed_mp(self, start_seed = 0, end_seed = 10000):
		# Define variables
		cpu_count = mp.cpu_count()
		diff = ceil((end_seed - start_seed) / cpu_count)
		results = mp.Manager().dict()

		# Create processes
		processes = []
		for i in range(cpu_count):
			process = mp.Process(target = self.find_best_seed, args = (i * diff, (i + 1) * diff, 3, i, results))
			processes.append(process)
			process.start()

		# Join processes and obtain best seed
		for process in processes:
			process.join()
		best_seed = min(results.values(), key = lambda t: t[1])[0]

		# Print result
		print(f"[BSPBuilder] Best seed is #{best_seed}")

		# Return
		return best_seed

	# Add segment
	def add_segment(self, node, segment):
		self.segments.append(segment)
		node.id = self.id
		self.id += 1

	# Split space
	def split_space(self, node, segments):
		# Define variables
		front_segments, back_segments = [], []

		# Set first segment as splitter
		node.splitter = segments[0]

		# Iterate over remaining segments
		for segment in segments[1:]:
			# Calculate numerator and denominator
			numerator = cross_2d(segment.start - node.splitter.start, node.splitter.get_vector())
			denominator = cross_2d(node.splitter.get_vector(), segment.get_vector())

			# Zero flags
			is_numerator_zero = abs(numerator) < EPS
			is_denominator_zero = abs(denominator) < EPS

			# Categorize segment
			if is_denominator_zero and is_numerator_zero:
				front_segments.append(segment)
				continue

			if not is_denominator_zero:
				t = numerator / denominator
				if 0 < t < 1:
					self.split_count += 1
					intersection = segment.start + t * segment.get_vector()
					front_segment = copy(segment)
					front_segment.end = intersection
					back_segment = copy(segment)
					back_segment.start = intersection

					if numerator > 0:
						back_segment, front_segment = front_segment, back_segment

					front_segments.append(front_segment)
					back_segments.append(back_segment)
					continue

			if numerator < 0 or (is_numerator_zero and denominator > 0):
				front_segments.append(segment)
			elif numerator > 0 or (is_numerator_zero and denominator < 0):
				back_segments.append(segment)

		# Return
		self.add_segment(node, node.splitter)
		return front_segments, back_segments

	# Build tree
	def build_tree(self, node, segments):
		# Check segment exist
		if not segments:
			return None

		# Categorize segments into front and back
		front_segments, back_segments = self.split_space(node, segments)

		# Recurse
		if back_segments:
			self.back_count += 1
			node.back = BSPNode()
			self.build_tree(node.back, back_segments)
		if front_segments:
			self.front_count += 1
			node.front = BSPNode()
			self.build_tree(node.front, front_segments)

# BSP traverser class
class BSPTraverser:
	# Constructor
	def __init__(self, engine):
		# Define properties
		self.engine = engine
		self.root = BSPNode()
		self.segments = []

		# Temporary
		self.pos = vec2(4, 4)
		self.ids = []

		# Initialize
		self.fetch()

	# Fetch data from engine
	def fetch(self):
		if self.engine.bsp_builder is not None:
			self.root = self.engine.bsp_builder.root
			self.segments = self.engine.bsp_builder.segments

	# Traverse function
	def traverse(self, node):
		# Check node
		if node is None:
			return

		# Check front
		front = is_front(self.pos - node.splitter.start, node.splitter.get_vector())
		if front:
			self.traverse(node.front)
			self.ids.append(node.id)
			self.traverse(node.back)
		else:
			self.traverse(node.back)
			self.ids.append(node.id)
			self.traverse(node.front)

	# Update function
	def update(self):
		self.ids.clear()
		self.traverse(self.root)
