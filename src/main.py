import game
import utils
import genetic_algorithm as ga
import numpy as np
import snake
import argparse
import human


def main():

	# adding parser
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group()
	group.add_argument("-p", "--play", action="store_true", help="play the base game")
	group.add_argument("-t", "--train", action="store_true", help="train a new model")
	group.add_argument("-l", "--load", action="store_true", help="load an existing model")

	parser.add_argument("-v", "--view", action="store_true", help="activate window representation")

	parser.add_argument("-s", "--size", default=20,
						help="specifies game size", action="store", type=int)

	parser.add_argument("-g", "--generations", default=10,
						help="specifies number of generations in the trained model",
						action="store", type=int)

	parser.add_argument("-k", "--snakes", default=10,
						help="specifies number of snakes per generation in the trained model",
						action="store",	type=int)

	parser.add_argument("-n", "--nn", nargs="*", default=[],
						help="specifies neural network hidden layers in the trained model",
						action="store", type=int)

	parser.add_argument("-e", "--end", default=100,
						help="specifies max duration of the game in the trained model",
						action="store", type=int)

	parser.add_argument("-m", "--name", default="generation",
						help="specifies name of the file in which store the model",
						action="store", type=str)

	args = parser.parse_args()

	# parser option for a simple game
	if args.play:

		g = game.game(args.size, True, np.inf)
		sn = snake.snake(human.human())
		g.add_snake(sn)

		while g.snake.is_alive:
			g.play()
			utils.esc_exit()

		print("Your total points are:", g.snake.fitness+1)

	# parser option to train a model
	elif args.train:

		best_generation, details = utils.train(snakes=args.snakes, shape=args.nn,
										generations=args.generations, size=args.size,
										view=args.view, end=args.end)

		utils.save(best_generation, details, args.name)
		
	# parser option to load an existing model
	elif args.load:

		generation, details = utils.load(args.name)
		print()
		print(args.name, "correctly loaded! Model details are:")
		print(details)

		print()
		train_answer = utils.get_yes_no("Do you want to continue to train the model?")

		if train_answer:

			print()
			generations = input("Insert number of generations to train: ")
			if not generations.isdigit():
				raise TypeError("Expected a digit, received a " + type(generations).__name__)
			generations = int(generations)

			best_generation, details = utils.train(generation, details, generations=generations,
											view=args.view)

			best_generation = ga.sort_generation(best_generation)

			utils.save(best_generation, details, args.name)

		else:

			print()
			view_answer = utils.get_yes_no("Do you want to view the model in action?")
			if not view_answer:
				exit()

			print()
			best_answer = utils.get_yes_no("Do you want to see only the best one?")
			if best_answer:

				g = game.game(details["game_size"], True, details["duration"])
				g.add_snake(generation[0])

				while g.snake.is_alive:
					g.play()
					utils.esc_exit()

				print("Snake points are:", g.snake.fitness)

			else:

				for sn in generation:

					g = game.game(details["game_size"], True, details["duration"])
					g.add_snake(sn)

					while g.snake.is_alive:
						g.play()
						utils.esc_exit()

					print("Snake points are:", g.snake.fitness)
			
	else:

		print("Please run with --help flag to see available options")


if __name__ == "__main__":
	main()