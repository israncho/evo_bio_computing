from sys import argv
from math import inf
from time import time
from src.gen_algo_framework.replacement import all_replacement_funcs
from src.tsp.ga_for_euclidean_tsp import genetic_algorithm_for_euctsp, __write_results
from src.utils.input_output import write_line_to_csv_file


ITERATIONS = 30
all_instances = ['berlin52', 'ch130', 'eil51', 'kroA100', 'pr152']
general_output_path = 'results/tsp/'
general_instance_path = 'instances/euc_TSP/'
memetic_params = {'replacement': 'full_gen_replacement_elitist',
                  'pop_size': 15,
                  'gens': 15,
                  'mutation_proba': 0.01,
                  'local_s_iters': 3,
                  'max_records': 2000,
                  'seed': None}

params = {'berlin52':
                {'full_gen_replacement_elitist': (50, 17000, 0.01), 'full_generational_replacement': (50, 17000, 0.01), 'replacement_of_the_worst': (250, 3400, 0.2)},
          'ch130':
                {'full_gen_replacement_elitist': (55, 100000, 0.01), 'full_generational_replacement': (55, 100000, 0.01), 'replacement_of_the_worst': (250, 22000, 0.2)},
          'eil51':
                {'full_gen_replacement_elitist': (55, 14600, 0.01), 'full_generational_replacement': (55, 14600, 0.01), 'replacement_of_the_worst': (250, 3200, 0.2)},
          'kroA100':
                {'full_gen_replacement_elitist': (50, 65000, 0.01), 'full_generational_replacement': (50, 65000, 0.01), 'replacement_of_the_worst': (250, 13000, 0.2)},
          'pr152':
                {'full_gen_replacement_elitist': (55, 140000, 0.01), 'full_generational_replacement': (55, 140000, 0.01), 'replacement_of_the_worst': (250, 30300, 0.2)}}


all_replacement_funcs_names = list(all_replacement_funcs.keys())
all_replacement_funcs_names.insert(0, 'memetic')


start_total_time = time()
for instance_name in all_instances:
    print('-----------------------------\n', instance_name, '\n--------------------------------\n')
    instance_file_path = general_instance_path + instance_name + '.tsp'
    for replacement_name in all_replacement_funcs_names:

        if replacement_name != 'memetic':
            pop_size, gens, mutation_proba = params[instance_name][replacement_name]
            instance: dict = {}
            instance['pop_size'] = pop_size
            instance['gens'] = gens
            instance['mutation_proba'] = mutation_proba
            instance['local_s_iters'] = 0
            instance['replacement'] = replacement_name
            instance['max_records'] = 2000
            instance['seed'] = None
        else:
            instance = memetic_params

        print('>>>>>>>>>\n', '>>>>>>>>>', replacement_name, '\n>>>>>>>>>\n')
        current_output_path = general_output_path + instance_name + '/'
        current_best = inf, None
        times = []
        seeds = []
        for i in range(ITERATIONS):
            print('\niteration:', i + 1)
            start = time()
            result, data = genetic_algorithm_for_euctsp(instance_file_path,
                                                        instance)
            end = time()
            runtime_secs = round(end - start, 4)
            total_runtime = round(end - start_total_time, 4)
            print('runtime in seconds:', runtime_secs, ',\ttotal runtime in mins:', total_runtime / 60)
            print('best fitness found:', result[0])
            print('f_execs:', data['f_execs'],
                  ', pop_size:', data['pop_size'],
                  ', gens:', data['gens'],
                  ', mutation_proba:', data['mutation_proba'],
                  ', local_s_iters:', data['local_s_iters'],
                  ', seed:', data['seed'])
            print('record size:', len(data['best_fitness_found_history']))

            write_solution = False
            if result[0] < current_best[0]:
                write_solution = True
                current_best = result

            __write_results(result, data, current_output_path + replacement_name, write_mode='a', write_solution=write_solution)

            times.append(runtime_secs)
            seeds.append(data['seed'])

        write_line_to_csv_file(current_output_path + 'seeds.csv', seeds)
        write_line_to_csv_file(current_output_path + 'times.csv', times)
