'''
Module to execute the GA for euclidean tsp
instances.
'''

from sys import argv
from ast import literal_eval
from src.gen_algo_framework.crossover import pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.gen_algo_framework.mutation import swap_mutation_population
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.tsp.euclidean_tsp import euc_tsp_fitness_maximization
from src.tsp.euclidean_tsp import simple_euc_tsp_options_handler
from src.tsp.visualization import animate_tsp_evolution
from src.utils.input_output import parse_tsp_data, read_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use

if __name__ == "__main__":
    FILE_PATH = argv[1]
    print(FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]
    PARAMS = literal_eval(argv[3])

    instance = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))

    POP_SIZE = PARAMS['pop_size']
    GENS = PARAMS['gens']
    SEED = seed_in_use(PARAMS['seed'])
    REPLACEMENT_F_NAME: str = PARAMS['replacement']


    replacement = all_replacement_funcs[REPLACEMENT_F_NAME]


    initial_population = generate_population_of_permutations(POP_SIZE, instance['rest_of_cities'])

    instance = simple_euc_tsp_options_handler(initial_population,
                                              instance,
                                              True,
                                              POP_SIZE,
                                              POP_SIZE,
                                              0.1)

    list_best_solutions_per_gen = genetic_algorithm(initial_population,
                      pop_crossover_ox1_roulettew_s, # pyright: ignore
                      swap_mutation_population, # pyright: ignore
                      euc_tsp_fitness_maximization, # pyright: ignore
                      replacement, # pyright: ignore
                      lambda gen_count, _ : gen_count < GENS,
                      simple_euc_tsp_options_handler,
                      instance)
    print('avg of the fitness of last generation:', instance['population_fit_avgs'][-1])
    print('fitness of best solution found:\n', instance['current_best'][0])
    print('used seed:', SEED)



    best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], list_best_solutions_per_gen))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    gen_best_line = generate_line_from_data(instance['gen_fittest_fitness'])

    labels = ['avg_fitness', 'gen_fittest_fitness', 'best_found']

    lines = [avg_fitness_line, gen_best_line, best_solutions_line]
    plot_evolution(lines, instance, OUTPUT_FILE_PATH, labels)

    only_permutations = list(map(lambda x: x[1], list_best_solutions_per_gen)) # pyright: ignore
    animate_tsp_evolution(instance, only_permutations, OUTPUT_FILE_PATH, 30) # pyright: ignore
