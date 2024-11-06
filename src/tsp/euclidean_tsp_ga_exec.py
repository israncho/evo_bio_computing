'''
Module to execute the GA for euclidean tsp
instances.
'''

from sys import argv
from ast import literal_eval
from time import time
from src.gen_algo_framework.crossover import pop_crossover_ox1_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm, standard_fitness_computing
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.gen_algo_framework.mutation import swap_mutation_population
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.tsp.euclidean_tsp import simple_euc_tsp_options_handler
from src.tsp.visualization import animate_tsp_evolution, plot_tsp_solution
from src.utils.input_output import parse_tsp_data, read_file, tsp_solution_to_lines, write_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use


def ga_exec_for_euctsp(file_path: str, # pyright: ignore
                       output_file_path: str,
                       params: dict,
                       write_solution: bool = False,
                       plot_generational_evo: bool = False,
                       plot_detailed_evo: bool = False,
                       plot_final_solution: bool = False,
                       animate_evo: bool = False):
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
    local_search_iters = params['local_s_iters']

    print(params)

    initial_population = generate_population_of_permutations(population_size,
                                                             instance['rest_of_cities'])

    instance = simple_euc_tsp_options_handler(initial_population,
                                              instance,
                                              init=True,
                                              offspring_s=population_size,
                                              next_gen_pop_s=population_size,
                                              mutation_proba=mutation_p,
                                              local_s_iters=local_search_iters)

    start = time()
    best_sols_per_gen = genetic_algorithm(initial_population,
                                          pop_crossover_ox1_roulettew_s, # pyright: ignore
                                          swap_mutation_population, # pyright: ignore
                                          standard_fitness_computing, # pyright: ignore
                                          replacement_f, # pyright: ignore
                                          lambda gen_count, _ : gen_count < generations,
                                          simple_euc_tsp_options_handler,
                                          instance)
    end = time()

    print('\nbest found value for f(x) =', best_sols_per_gen[-1][0])
    print('last generation avg value of f(x) =', instance['population_fit_avgs'][-1])
    print('target function executions:', instance['f_execs'])
    print('execution time:', end - start, 'secs\n')

    # plotting performance
    best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], best_sols_per_gen))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    gen_best_line = generate_line_from_data(instance['gen_fittest_fitness'])
    labels = ['avg_fitness', 'gen_fittest_fitness', 'best_found']
    lines = [avg_fitness_line, gen_best_line, best_solutions_line]

    # generational evolution
    if plot_generational_evo:
        plot_evolution(lines, params, output_file_path, labels)

    # detailed evolution
    if plot_detailed_evo:
        detailed_best_solutions_line = generate_line_from_data(instance['best_fitness_found_history'])
        plot_evolution([detailed_best_solutions_line],
                   params,
                   output_file_path + '_detailed',
                   ['best_found'],
                   x_label='target_function_execs',
                   x_logscale=True)


    # writing best solution
    if write_solution:
        write_file(output_file_path + f'_solution_{instance['NAME']}.txt',
               tsp_solution_to_lines(instance['fst_city'],
                                     best_sols_per_gen[-1][1], # pyright: ignore
                                     instance))
    if plot_final_solution:
        plot_tsp_solution(instance, best_sols_per_gen[-1][1], output_file_path) # pyright: ignore

    # animating best solution progress
    if animate_evo:
        only_permutations = list(map(lambda x: x[1], best_sols_per_gen)) # pyright: ignore
        animate_tsp_evolution(instance, only_permutations, output_file_path, 2) # pyright: ignore


if __name__ == "__main__":
    FILE_PATH = argv[1]
    OUTPUT_FILE_PATH = argv[2]
    PARAMS = literal_eval(argv[3])

    ga_exec_for_euctsp(FILE_PATH,
                       OUTPUT_FILE_PATH,
                       PARAMS,
                       True,
                       True,
                       True,
                       True,
                       True)
