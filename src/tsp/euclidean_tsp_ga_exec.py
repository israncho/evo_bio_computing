from sys import argv
from src.gen_algo_framework.crossover import pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.genetic_algorithm import generate_population
from src.gen_algo_framework.mutation import swap_mutation_population
from src.gen_algo_framework.replacement import full_generational_replacement
from src.tsp.euclidean_tsp import euc_tsp_fitness_maximization, simple_euc_tsp_options_handler
from src.tsp.visualization import animate_tsp_evolution
from src.utils.input_output import parse_tsp_data, read_file

if __name__ == "__main__":
    FILE_PATH = argv[1]
    print(FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]

    instance = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))


    initial_population = generate_population(10000, instance['rest_of_cities'])

    instance = simple_euc_tsp_options_handler(initial_population, instance, init=True)

    best_sol = genetic_algorithm(initial_population,
                      pop_crossover_ox1_roulettew_s, # pyright: ignore
                      swap_mutation_population, # pyright: ignore
                      euc_tsp_fitness_maximization, # pyright: ignore
                      full_generational_replacement,
                      lambda gen_count, _ : gen_count < 250,
                      simple_euc_tsp_options_handler,
                      instance)
    print(instance['population_fit_avgs'])

    only_permutations = list(map(lambda x: x[1], best_sol)) # pyright: ignore
    animate_tsp_evolution(instance, only_permutations, OUTPUT_FILE_PATH)
