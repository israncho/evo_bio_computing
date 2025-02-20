from sys import argv
from ast import literal_eval
from src.utils.input_output import parse_tsp_data, read_file
from src.utils.others import seed_in_use
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
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


if __name__ == "__main__":
    print()
    INSTANCE_FILE_PATH = argv[1]
    print(INSTANCE_FILE_PATH)
    OUTPUT_FILE_PATH = argv[2]
    print('output path:', OUTPUT_FILE_PATH)
    PARAMS = literal_eval(argv[3])

    result, data = genetic_algorithm_for_euctsp(INSTANCE_FILE_PATH,
                                                OUTPUT_FILE_PATH,
                                                PARAMS)
    print('best fitness found:', result[0])
