'''

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
#from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.utils.others import seed_in_use
from src.utils.input_output import write_file, list_to_line
from src.continuous.functions import all_funcs

def multiple_ga_execs(params: dict, output_file_path: str):

    func_name: str = params['f']
    pop_size: int = params['pop_size']
    gens: int = params['gens']
    dimension: int = params['dim']
    n_bits_p_entry: int = params['n_bits']
    interval: tuple = params['interval']
    crossover_n_points: int = params['crossover_n_p']
    mutation_p: float = params['mutation_p']
    seed = seed_in_use(params['seed'])
    params['seed'] = seed
    reps: int = params['reps']
    replacement_f_name: str = params['replacement']
    params['NAME'] = func_name

    print('\n', params)

    v_n_bits = [n_bits_p_entry] * dimension
    v_intervals = [interval] * dimension

    f = all_funcs[func_name]

    replacement = all_replacement_funcs[replacement_f_name]

    write_file(output_file_path,[str(params) + '\n'])

    for i in range(reps):
        print('\nRep:', i + 1)

        instance = {'NAME': func_name, 'seed': seed}

        initial_population = generate_population_of_bit_vectors(pop_size, v_n_bits)

        instance = simple_c_f_options_handler(
            initial_population,
            instance,
            True,
            pop_size,
            pop_size,
            mutation_p,
            f,
            crossover_n_points,
            v_n_bits,
            v_intervals)

        list_best_solutions_per_gen = genetic_algorithm(
            initial_population,
            population_n_points_crossover_roulettew_s, # pyright: ignore
            bit_flip_mutation_population, # pyright: ignore
            compute_vectors_fitness, # pyright: ignore
            replacement, # pyright: ignore
            lambda gen_count, _ : gen_count < gens,
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
        write_file(output_file_path, [gen_results], mode='a')

        '''
        best_solutions_line = generate_line_from_data(list(map(
        lambda x: x[0], list_best_solutions_per_gen))) # pyright: ignore
        avg_fitness_line = generate_line_from_data(instance['population_fit_avgs'])
        labels = ['avg_fitness', 'best_found']

        lines = [avg_fitness_line, best_solutions_line]
        plot_evolution(lines, instance, output_file_path + str(i), labels)
        '''
    

if __name__ == "__main__":
    output_file_path: str = argv[1]
    params: dict = literal_eval(argv[2])

    multiple_ga_execs(params, output_file_path)
   
