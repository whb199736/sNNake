from snake import *


def neural_network_crossover(neural_network_a, neural_network_b, crossover_prob=0.95, mutation_prob=0.01):
	"""
	Used to mix two neural networks as part of the genetic algorithm

	Parameters
	----------
	neural_network_a : neuralnet
		first neural network to mix
	neural_network_b : neuralnet
		second neural network to mix
	crossover_prob : float
		probability of crossover
	mutation_prob : float
		probability of mutation
	"""

	assert isinstance(neural_network_a, neuralnet), "Expected a neuralnet, received a " + type(neural_network_a).__name__
	assert isinstance(neural_network_b, neuralnet), "Expected a neuralnet, received a " + type(neural_network_b).__name__
	assert neural_network_a.shape == neural_network_b.shape, "Neural networks don't have the same shape"
	assert 1 >= crossover_prob >= 0, "Wrong crossover probability value: not between 0 and 1"
	assert 1 >= mutation_prob >= 0, "Wrong mutation probability value: not between 0 and 1"

	weights = []

	for i in range(len(neural_network_a.shape)-1):

		neural_network_a_genes = neural_network_a.weights[i].flatten()
		neural_network_b_genes = neural_network_b.weights[i].flatten()

		if np.random.rand() < crossover_prob:

			# perform a crossover
			crossover = np.random.randint(0, len(neural_network_a_genes))
			temp = neural_network_a_genes[crossover:len(neural_network_a_genes)+1].copy()

			neural_network_a_genes[crossover:len(neural_network_a_genes)+1] = neural_network_b_genes[crossover:len(neural_network_b_genes)+1]
			neural_network_b_genes[crossover:len(neural_network_b_genes)+1] = temp

		if np.random.rand() < mutation_prob:

			# perform a mutation
			m = np.random.randint(0, len(neural_network_a_genes))
			mutation = np.random.uniform(-1, 1)

			neural_network_a_genes[m] = mutation
			neural_network_b_genes[m] = mutation

		# decide which neural network is returned
		if np.random.choice([-1, 1]) > 0:
			weights.append(neural_network_a_genes.reshape(neural_network_a.weights[i].shape))
		else:
			weights.append(neural_network_b_genes.reshape(neural_network_b.weights[i].shape))
 
	neuralnet_final = neuralnet(neural_network_a.shape, False, weights)

	return neuralnet_final


def sort_generation(generation):
	"""
	Sorts the generation by fitness in decreasing order
	"""

	assert isinstance(generation, list), "Expected a list, received a " + type(generation).__name__
	for element in generation:
		assert isinstance(element, snake), "Expected a snake, received a " + type(element).__name__

	generation.sort(key=lambda snake: snake.fitness, reverse=True)

	return generation


def create_generation(generation, snakes=10, nn=[], q=0.05, crossover_prob=0.95, mutation_prob=0.01):
	"""
	Creates a new generation out of the previous one
	"""
	assert 1 >= crossover_prob >= 0, "Wrong crossover probability value: not between 0 and 1"
	assert 1 >= mutation_prob >= 0, "Wrong mutation probability value: not between 0 and 1"
	assert 1 >= q >= 0, "Wrong choose element probability value: not between 0 and 1"
	assert isinstance(generation, list), "Expected a list, received a " + type(generation).__name__
	for element in generation:
		assert isinstance(element, snake), "Expected a snake, received a " + type(snake).__name__

	if not generation:

		for i in range(snakes):
			generation.append(snake(nn))

		return generation

	else:

		generation = sort_generation(generation)

		# creating the probability vector
		p = np.fromfunction(lambda r: q*(1-q)**r, shape=(len(generation),))
		p = p/p.sum()

		new_generation = []

		for i in range(len(generation)):

			neural_network_a = np.random.choice(generation, p=p).neural_network
			neural_network_b = np.random.choice(generation, p=p).neural_network

			neural_network_final = neural_network_crossover(neural_network_a, neural_network_b, crossover_prob, mutation_prob)

			snake_final = snake(neural_network_final)

			new_generation.append(snake_final)

		return new_generation