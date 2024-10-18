'''

'''


from sys import argv
from ast import literal_eval
from src.continuous.binary_representation import decode_vector
from src.continuous.functions import c_f_fitness_maximization, simple_c_f_options_handler
from src.gen_algo_framework.crossover import population_n_points_crossover_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.population_utils import generate_population_of_bit_vectors
from src.gen_algo_framework.mutation import bit_flip_mutation_population
from src.gen_algo_framework.replacement import all_replacement_funcs
#from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use
from src.utils.input_output import write_file, list_to_line
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
    REPS: int = PARAMS['reps']
    REPLACEMENT_F_NAME: str = PARAMS['replacement']

    print('\n', PARAMS)

    v_n_bits = [N_BITS_P_ENTRY] * DIMENSION
    v_intervals = [INTERVAL] * DIMENSION

    f = all_funcs[FUNC_NAME]

    replacement = all_replacement_funcs[REPLACEMENT_F_NAME]

    write_file(OUTPUT_FILE_PATH,[str(PARAMS) + '\n'])

    for i in range(REPS):
        print('\nRep:', i + 1)

        instance = {'NAME': FUNC_NAME, 'SEED': SEED}

        initial_population = generate_population_of_bit_vectors(POP_SIZE, v_n_bits)

        instance = simple_c_f_options_handler(
            initial_population,
            instance,
            True,
            POP_SIZE,
            POP_SIZE,
            MUTATION_P,
            f,
            CROSSOVER_NUM_POINTS,
            v_n_bits,
            v_intervals)

        list_best_solutions_per_gen = genetic_algorithm(
            initial_population,
            population_n_points_crossover_roulettew_s, # pyright: ignore
            bit_flip_mutation_population, # pyright: ignore
            c_f_fitness_maximization, # pyright: ignore
            replacement, # pyright: ignore
            lambda gen_count, _ : gen_count < GENS,
            simple_c_f_options_handler,
            instance)

        print('------ Best f(x) =', list_best_solutions_per_gen[-1][0])
        print('Last generation\'s avg f(x) =', instance['population_fit_avgs'][-1])
        print('x =', decode_vector(list_best_solutions_per_gen[-1][1], # pyright: ignore
                                   v_n_bits,
                                   v_intervals))

        instance['population_fit_avgs']
        list_fitness_best_sols_per_gen = list(map(lambda x: x[0], list_best_solutions_per_gen))
        gen_results = list_to_line(list(zip(list_fitness_best_sols_per_gen,
                                            instance['population_fit_avgs'])) + ['\n']) # pyright: ignore
        write_file(OUTPUT_FILE_PATH, [gen_results], mode='a')

        '''
        best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], list_best_solutions_per_gen))) # pyright: ignore
        avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
        labels = ['avg_fitness', 'best_found']

        lines = [avg_fitness_line, best_solutions_line]
        plot_evolution(lines, instance, OUTPUT_FILE_PATH + str(i), labels)
        '''
