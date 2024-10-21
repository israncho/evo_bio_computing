'''
Module to execute the GA for continuous
optimization functions.
'''


from sys import argv
from ast import literal_eval
from src.continuous.binary_representation import decode_vector
from src.continuous.functions import compute_vectors_fitness, simple_c_f_options_handler
from src.gen_algo_framework.crossover import population_n_points_crossover_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.population_utils import generate_population_of_bit_vectors
from src.gen_algo_framework.mutation import bit_flip_mutation_population
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.gen_algo_framework.diversity import all_distance_measures  
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use
from src.continuous.functions import all_funcs

if __name__ == "__main__":
    OUTPUT_FILE_PATH: str = argv[1]
    PARAMS: dict = literal_eval(argv[2])
    FUNC_NAME: str = PARAMS['f']
    POP_SIZE: int = PARAMS['pop_size']
    GENS: int = PARAMS['gens']
    DIMENSION: int = PARAMS['dim']
    N_BITS_P_ENTRY: int = PARAMS['n_bits']
    INTERVAL: tuple = PARAMS['interval']
    CROSSOVER_NUM_POINTS: int = PARAMS['crossover_n_p']
    MUTATION_P: float = PARAMS['mutation_p']
    SEED = seed_in_use(PARAMS['seed'])
    PARAMS['seed'] = SEED
    REPLACEMENT_F_NAME: str = PARAMS['replacement']
    
    CALC_ENTROPY = PARAMS['entropy']
    DISTANCE_MEASURE_NAME = PARAMS['distance_m']
    print(PARAMS)

    replacement = all_replacement_funcs[REPLACEMENT_F_NAME]

    v_n_bits = [N_BITS_P_ENTRY] * DIMENSION
    v_intervals = [INTERVAL] * DIMENSION

    f = all_funcs[FUNC_NAME]

    if DISTANCE_MEASURE_NAME is None:
        distance_measure = None
    else:
        distance_measure = all_distance_measures[DISTANCE_MEASURE_NAME]

    initial_population = generate_population_of_bit_vectors(POP_SIZE, v_n_bits)

    PARAMS['NAME'] = FUNC_NAME
    instance = {}

    instance = simple_c_f_options_handler(initial_population,
                                          instance,
                                          True,
                                          POP_SIZE,
                                          POP_SIZE,
                                          MUTATION_P,
                                          f,
                                          CROSSOVER_NUM_POINTS,
                                          v_n_bits,
                                          v_intervals,
                                          True,
                                          CALC_ENTROPY,  
                                          distance_measure)

    list_best_solutions_per_gen = genetic_algorithm(initial_population,
                      population_n_points_crossover_roulettew_s, # pyright: ignore
                      bit_flip_mutation_population, # pyright: ignore
                      compute_vectors_fitness, # pyright: ignore
                      replacement, # pyright: ignore
                      lambda gen_count, _ : gen_count < GENS,
                      simple_c_f_options_handler,
                      instance)

    print('avg of the fitness of last generation:', instance['population_fit_avgs'][-1])
    print('fitness of best solution found:\n', instance['current_best'][0])
    print('best solution found:',
          decode_vector(list_best_solutions_per_gen[-1][1], v_n_bits, v_intervals)) # pyright: ignore
    print('used seed:', SEED)

    best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], list_best_solutions_per_gen))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    gen_best_line = generate_line_from_data(instance['gen_fittest_fitness'])
    labels = ['avg_fitness', 'gen_fittest_fitness', 'best_found']

    lines = [avg_fitness_line, gen_best_line, best_solutions_line]
    plot_evolution(lines, PARAMS, OUTPUT_FILE_PATH, labels)

    if instance['pop_entropy'] is not None:
        entropy_line = generate_line_from_data(instance['pop_entropy'])
        plot_evolution([entropy_line], PARAMS, OUTPUT_FILE_PATH + 'entropy', ['population_entropy'], 'population_entropy')

    if instance['pop_diversity'] is not None:
        diversity_line = generate_line_from_data(instance['pop_diversity'])
        plot_evolution([diversity_line], PARAMS, OUTPUT_FILE_PATH + 'diversity', ['population_diversity'], 'population_diversity')