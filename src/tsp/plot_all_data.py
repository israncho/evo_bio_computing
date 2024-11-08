
from src.utils.input_output import read_lines_from_csv_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution


all_instances = ['berlin52', 'ch130', 'eil51', 'kroA100', 'pr152']
default_params = {'replacement': 'full_gen_replacement_elitist',
                  'seed': None,
                  'pop_size': 20,
                  'gens': 20,
                  'mut_p': 0.1,
                  'local_s_iters': 3}

general_data_path = 'results/tsp/'


for instance in all_instances:
    print(instance)
    default_params['NAME'] = instance
    executions_data_path = general_data_path + instance + f'/memetic_{instance}_data.csv'
    accumulated_sum = None
    number_executions = 0
    for single_exec in read_lines_from_csv_file(executions_data_path):
        number_executions += 1
        if accumulated_sum is None:
            accumulated_sum = single_exec
        else:
            accumulated_sum += single_exec
    avgs = accumulated_sum / number_executions # pyright: ignore
    line = generate_line_from_data(avgs)
    plot_evolution([line],
                   default_params,
                   general_data_path + instance + '/comparison',
                   ['avg_best_fitness_found_memetic_algo'],
                   x_label='target_function_executions',
                   x_logscale=True)
