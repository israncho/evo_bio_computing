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
from src.utils.input_output import parse_tsp_data, read_file, tsp_solution_to_lines, write_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use


def ga_exec_for_euctsp(file_path: str, # pyright: ignore
                       output_file_path: str,
                       params: dict):
    '''
    Genetic algoirthm execution for eucTSP. Computes
    and Generates the performance plot, animates the
    best individuals and saves the best solution found
    '''
    print(file_path)
    instance = parse_tsp_data(read_file(file_path))
    print(f'Output files path: {output_file_path}')
    params['NAME'] = instance['NAME']

    population_size = params['pop_size']
    generations = params['gens']
    seed = seed_in_use(params['seed'])
    params['seed'] = seed
    mutation_p = params['mut_p']
    replacement_f_name: str = params['replacement']

    replacement_f = all_replacement_funcs[replacement_f_name]

    print(params)

    initial_population = generate_population_of_permutations(population_size,
                                                             instance['rest_of_cities'])

    instance = simple_euc_tsp_options_handler(initial_population,
                                              instance,
                                              init=True,
                                              offspring_s=population_size,
                                              next_gen_pop_s=population_size,
                                              mutation_proba=mutation_p)

    best_sols_per_gen = genetic_algorithm(initial_population,
                                          pop_crossover_ox1_roulettew_s, # pyright: ignore
                                          swap_mutation_population, # pyright: ignore
                                          euc_tsp_fitness_maximization, # pyright: ignore
                                          replacement_f, # pyright: ignore
                                          lambda gen_count, _ : gen_count < generations,
                                          simple_euc_tsp_options_handler,
                                          instance)

    print('best found value for f(x) =', best_sols_per_gen[-1][0])
    print('last generation avg value of f(x) =', instance['population_fit_avgs'][-1])

    # plotting performance
    best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], best_sols_per_gen))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    gen_best_line = generate_line_from_data(instance['gen_fittest_fitness'])
    labels = ['avg_fitness', 'gen_fittest_fitness', 'best_found']
    lines = [avg_fitness_line, gen_best_line, best_solutions_line]
    plot_evolution(lines, params, output_file_path, labels)

    # writing best solution
    write_file(output_file_path + f'_{instance['NAME']}.txt',
               tsp_solution_to_lines(instance['fst_city'],
                                     best_sols_per_gen[-1][1], # pyright: ignore
                                     instance))

    # animating best solution progress
    only_permutations = list(map(lambda x: x[1], best_sols_per_gen)) # pyright: ignore
    animate_tsp_evolution(instance, only_permutations, output_file_path, 10) # pyright: ignore


if __name__ == "__main__":
    FILE_PATH = argv[1]
    OUTPUT_FILE_PATH = argv[2]
    PARAMS = literal_eval(argv[3])

    ga_exec_for_euctsp(FILE_PATH, OUTPUT_FILE_PATH, PARAMS)
