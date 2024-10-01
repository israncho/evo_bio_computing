from sys import argv
from src.gen_algo_framework.crossover import pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.gen_algo_framework.mutation import swap_mutation_population
from src.gen_algo_framework.replacement import full_generational_replacement
from src.tsp.euclidean_tsp import euc_tsp_fitness_maximization, simple_euc_tsp_options_handler, tour_distance
from src.tsp.visualization import animate_tsp_evolution
from src.utils.input_output import parse_tsp_data, read_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution

if __name__ == "__main__":
    FILE_PATH = argv[1]
    print(FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]

    instance = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))

    POP_SIZE = 150

    initial_population = generate_population_of_permutations(POP_SIZE, instance['rest_of_cities'])

    instance = simple_euc_tsp_options_handler(initial_population, instance, True, POP_SIZE, POP_SIZE)

    best_sol = genetic_algorithm(initial_population,
                      pop_crossover_ox1_roulettew_s, # pyright: ignore
                      swap_mutation_population, # pyright: ignore
                      euc_tsp_fitness_maximization, # pyright: ignore
                      full_generational_replacement,
                      lambda gen_count, _ : gen_count < 750,
                      simple_euc_tsp_options_handler,
                      instance)
    print('Fitness of last generation\'s best individual:\n', instance['population_fit_avgs'][-1])



    best_solutions_line = generate_line_from_data(list(map(
        lambda x: tour_distance(instance['fst_city'], x[1], instance['weights']), best_sol))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    labels = ['avg_fitness', 'generational_best']

    lines = [avg_fitness_line, best_solutions_line]
    plot_evolution(lines, instance, OUTPUT_FILE_PATH, labels)

    only_permutations = list(map(lambda x: x[1], best_sol)) # pyright: ignore
    animate_tsp_evolution(instance, only_permutations, OUTPUT_FILE_PATH, 25)
