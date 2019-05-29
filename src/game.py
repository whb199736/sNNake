from snake import *

class game:
	"""
	Main class used to play the game Snake

	Attributes
	----------
	size : list
		a list of integers used to represent the game window
	background_color : tuple
		describes the background color of the game window
	snake_color : tuple
		describes the snake color in the game window
	food_color : tuple
		describes the food color in the game window
	clock : pygame.time object
		used to control the refresh of the game window
	window : pygame.display object
		used to represent the game

	Methods
	-------
	play()
		runs the game
	add_snake()
		creates a new snake
	add_food()
		creates new food
	represent(frequency=30)
		depicts the game window
	end()
		checks that the snake is still in the field and that has not
		eaten itself
	"""


	def __init__(self, size=[40, 20], duration=1e3):
		"""
		Parameters
		----------
		size : array
			size[0] is the number of squares in the game field
			size[1] is the size in pixels of each square
		"""

		self.size = np.array(size)
		self.step = 0
		self.duration = duration
		self.background_color = (202, 202, 202)
		self.snake_color = (66, 149, 71)
		self.food_color = (183, 43, 56)
		self.clock = pygame.time.Clock()
		self.window = pygame.display.set_mode((self.size[0]*self.size[1],
											self.size[0]*self.size[1]))


	def play(self):

		self.add_food()

		while self.snake.is_alive and self.snake.eat_not(self.food):

			self.snake.move(self.size, self.food)
			self.end()
			self.represent()


	def add_snake(self, ext_snake=None):

		if ext_snake == None:
			self.snake = snake()
			assert self.snake.is_alive
		else:
			self.snake = ext_snake


		# initialize position
		self.snake.position = np.random.randint(0, self.size[0], 2)
		self.snake.occupied.insert(0, self.snake.position.copy())


	def add_food(self):

		self.food = food()

		# initialize position and check to not create new food in snake
		self.food.position = np.random.randint(0, self.size[0], 2)
		while any((self.food.position == x).all() for x in self.snake.position):
			self.add_food()


	def represent(self, frequency=24):
		"""
		Parameters
		----------
		frequency : int
			refresh per second
		"""

		self.window.fill(self.background_color)

		# draws food
		pygame.draw.rect(self.window, self.food_color,
			pygame.Rect(self.food.position[1]*self.size[1], self.food.position[0]*self.size[1],
				self.size[1], self.size[1]))

		# draws snake
		for coord in self.snake.occupied:
			pygame.draw.rect(self.window, self.snake_color,
				pygame.Rect(coord[1]*self.size[1], coord[0]*self.size[1],
					self.size[1], self.size[1]))

		pygame.display.flip()
		assert type(frequency==int)
		self.clock.tick(frequency)


	def end(self):

		# checks if snake is still in the field
		if not (0 <= self.snake.position[0] < self.size[0] and
			0 <= self.snake.position[1] < self.size[0]):
			self.snake.fitness -= 1
			self.snake.is_alive = False

		# checks if snake has eaten itself
		if any((self.snake.position == x).all() for x in self.snake.occupied[1:]):
			self.snake.fitness -= 1
			self.snake.is_alive = False

		# checks if the game has ended
		if self.step < self.duration:
			self.step += 1
		else:
			self.snake.is_alive = False


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--size", nargs=2, default=[40, 20],
						help="specifies field size", action="store",
						type=int)

	args = parser.parse_args()

	G = game(args.size)
	sn = snake(True, (5, 2, 3))
	G.add_snake(sn)

	while G.snake.is_alive:
		
		G.play()


if __name__ == "__main__":
	main()