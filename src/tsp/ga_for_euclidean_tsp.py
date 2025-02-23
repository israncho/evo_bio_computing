from sys import argv
from time import time
from ast import literal_eval
from src.utils.input_output import parse_tsp_data, read_file, write_file, write_line_to_csv_file, tsp_solution_to_lines
from src.utils.others import seed_in_use
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm, population_fitness_computing
from src.gen_algo_framework.selection import roulette_wheel_selection
from src.gen_algo_framework.crossover import order_crossover_ox1
from src.gen_algo_framework.mutation import swap_mutation
from src.gen_algo_framework.population_utils import generate_population_of_permutations
from src.local_search.permutation import local_search_2_opt
from src.tsp.euclidean_tsp import tour_distance, simple_euc_tsp_options_handler


def genetic_algorithm_for_euctsp(instance_file_path: str,
                                 output_file_path: str,
                                 params: dict) -> None:

    instance: dict = parse_tsp_data(read_file(instance_file_path))
    for key, value in params.items():
        instance[key] = value

    instance['seed'] = seed_in_use(instance['seed'])

    fitness_function: callable = tour_distance
    if instance['local_s_iters'] > 0:
        fitness_function: callable = local_search_2_opt

    replacement_function: callable = all_replacement_funcs[instance['replacement']]

    initial_population = generate_population_of_permutations(instance['pop_size'], set(instance['rest_of_cities']))
    instance = simple_euc_tsp_options_handler(initial_population, instance, True)
    initial_population = population_fitness_computing(tour_distance, initial_population, instance)


    best_found = genetic_algorithm(population=initial_population,
                                   selection=roulette_wheel_selection,
                                   crossover=order_crossover_ox1,
                                   mutation=swap_mutation,
                                   fitness_f=fitness_function,
                                   replacement=replacement_function,
                                   term_cond=lambda gen_count, _ : gen_count < instance['gens'],
                                   options_handler=simple_euc_tsp_options_handler,
                                   options=instance)
    return best_found, instance


def __write_results(best_found, exec_data, output_file_path, write_mode='w') -> None:

    solution_file_path = output_file_path + f'_solution_{exec_data['NAME']}.txt'
    str_lines_to_write = tsp_solution_to_lines(exec_data['fst_city'], best_found[1], exec_data)
    write_file(solution_file_path, str_lines_to_write)

    csv_file_path = output_file_path + f'_{exec_data['NAME']}_data.csv'
    write_line_to_csv_file(csv_file_path, exec_data['best_fitness_found_history'], mode=write_mode)
    print(f"Written execution data in: '{csv_file_path}'")


if __name__ == "__main__":
    print()
    INSTANCE_FILE_PATH = argv[1]
    print(INSTANCE_FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]
    print('output path:', OUTPUT_FILE_PATH)
    PARAMS = literal_eval(argv[3])

    start = time()
    result, data = genetic_algorithm_for_euctsp(INSTANCE_FILE_PATH,
                                                OUTPUT_FILE_PATH,
                                                PARAMS)
    end = time()
    print('runtime in seconds:', end - start)
    print('best fitness found:', result[0])
    print('target fuction evals:', data['f_execs'])
    __write_results(result, data, OUTPUT_FILE_PATH)