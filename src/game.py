import snake
import food
import pygame
import numpy as np


class game:
	"""
	Main class used to play the game Snake

	Attributes
	----------
	size : int
		size of the game (in squares)
	_view : bool
		if True represent the game
	_step : int
		current duration of the game
	_duration : float
		max duration of the game
	_background_color : tuple
		describes the background color of the game window
	_snake_color : tuple
		describes the snake color in the game window
	_food_color : tuple
		describes the food color in the game window
	_clock : pygame.time object
		used to control the refresh of the game window
	window : pygame.display object
		used to represent the game

	Methods
	-------
	play()
		runs the game
	add_snake()
		creates a new snake
	_add_food()
		creates new food
	_represent(frequency=30)
		depicts the game window
	_is_over()
		checks if the snake is still in the field or if it has
		eaten itself
	"""


	def __init__(self, size=40, view=False, duration=1e3):
		"""
		Parameters
		----------
		size : array
			the number of squares in the game field
		view : bool
			if True represent the game
		duration : float
			max duration of the game
		"""

		if not isinstance(size, (int, float)):
			raise TypeError( "Expected an int or a float, received a " + type(size).__name__)
		if not isinstance(size, (int, float)):
			raise TypeError("Expected an int or a float, received a " + type(size).__name__)
		if not isinstance(duration, (int, float)):
			raise TypeError("Expected a int or a float, received a " + type(duration).__name__)

		self.size = size
		self._view = view
		self._step = 0
		self._duration = duration
		self._background_color = (202, 202, 202)
		self._snake_color = (66, 149, 71)
		self._food_color = (183, 43, 56)
		self._clock = pygame.time.Clock()

		if self._view:
			self._window = pygame.display.set_mode((self.size*20,
											self.size*20))


	def play(self):

		self._add_food()

		while self.snake.is_alive and self.snake.has_not_eaten_food(self.food):

			self._is_over()
			self.snake.move(self.size, self.food)

			if self._view:
				self._represent()


	def add_snake(self, ext_snake=None):

		if ext_snake == None:
			self.snake = snake.snake()
		else:
			if not isinstance(ext_snake, snake.snake):
				raise TypeError("Expected a snake, received a " + type(ext_snake).__name__)
			self.snake = ext_snake

		# initialize position
		self.snake.position = np.random.randint(0, self.size, 2)
		self.snake.occupied.insert(0, self.snake.position.copy())


	def _add_food(self):

		self.food = food.food()

		# initialize position and check to not create new food in snake
		self.food.position = np.random.randint(0, self.size, 2)
		while any((self.food.position == x).all() for x in self.snake.position):
			self._add_food()


	def _represent(self, frequency=24):
		"""
		Parameters
		----------
		frequency : int
			refreshes per second
		"""

		if not isinstance(frequency, (int, float)):
			raise TypeError("Expected an int or a float, received a " + type(frequency).__name__)

		self._window.fill(self._background_color)

		# drawing food
		pygame.draw.rect(self._window, self._food_color,
			pygame.Rect(self.food.position[1]*20, self.food.position[0]*20,
				20, 20))

		# drawing snake
		for coord in self.snake.occupied:
			pygame.draw.rect(self._window, self._snake_color,
				pygame.Rect(coord[1]*20, coord[0]*20,
					20, 20))

		pygame.display.flip()

		self._clock.tick(frequency)


	def _is_over(self):

		# checks if the snake is still in the field
		if self.snake.has_exited(self.size):
			self.snake.dies()

		# checks if the snake has eaten itself
		if self.snake.has_eaten_himself():
			self.snake.dies()

		# checks if the game has ended for reaching max duration
		if self._step >= self._duration:
			self.snake.dies()
		else:
			self._step += 1