'''
'''

from sys import argv
from src.continuous.binary_representation import decode_vector
from src.continuous.functions import c_f_fitness_maximization, simple_c_f_options_handler
from src.gen_algo_framework.crossover import population_n_points_crossover_roulettew_s
from src.gen_algo_framework.genetic_algorithm import genetic_algorithm
from src.gen_algo_framework.population_utils import generate_population_of_bit_vectors
from src.gen_algo_framework.mutation import bit_flip_mutation_population
from src.gen_algo_framework.replacement import full_gen_replacement_elitist
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.continuous.functions import all_funcs

if __name__ == "__main__":
    FUNC_NAME = argv[1]
    print(FUNC_NAME)
    OUTPUT_FILE_PATH = argv[2]


    DIMENSION = 5

    v_n_bits = [25] * DIMENSION
    v_intervals = [(-30.0, 30.0)] * DIMENSION
    NUM_POINTS = 7

    f = all_funcs[FUNC_NAME]

    POP_SIZE = 1000

    initial_population = generate_population_of_bit_vectors(POP_SIZE, v_n_bits)

    instance = {'NAME': FUNC_NAME, 'n_points': NUM_POINTS}

    instance = simple_c_f_options_handler(initial_population,
                                          instance,
                                          v_n_bits,
                                          v_intervals,
                                          f,
                                          True,
                                          POP_SIZE,
                                          POP_SIZE)

    best_sol = genetic_algorithm(initial_population,
                      population_n_points_crossover_roulettew_s, # pyright: ignore
                      bit_flip_mutation_population, # pyright: ignore
                      c_f_fitness_maximization, # pyright: ignore
                      full_gen_replacement_elitist, # pyright: ignore
                      lambda gen_count, _ : gen_count < 200,
                      simple_c_f_options_handler,
                      instance)

    print('avg of the fitness of last generation:', instance['population_fit_avgs'][-1])
    print('fitness of best solution found:\n', instance['current_best'][0])
    print('best solution found:',
          decode_vector(best_sol[-1][1], v_n_bits, v_intervals)) # pyright: ignore


    best_solutions_line = generate_line_from_data(list(map(
        lambda x: f(decode_vector(x[1], v_n_bits, v_intervals)), best_sol))) # pyright: ignore
    avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
    labels = ['avg_fitness', 'best_found']

    lines = [avg_fitness_line, best_solutions_line]
    plot_evolution(lines, instance, OUTPUT_FILE_PATH, labels)
