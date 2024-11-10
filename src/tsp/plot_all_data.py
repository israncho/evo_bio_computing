
from numpy import ndarray
from src.utils.input_output import read_lines_from_csv_file
from src.utils.plot_functions import generate_line_from_data, plot_evolution


def get_performance_avgs_for_executions(executions_data_path: str) -> ndarray:
    accumulated_sum = None
    number_executions = 0
    for single_exec in read_lines_from_csv_file(executions_data_path):
        number_executions += 1
        if accumulated_sum is None:
            accumulated_sum = single_exec
        else:
            accumulated_sum += single_exec
    return accumulated_sum / number_executions # pyright: ignore



all_instances = ['berlin52', 'ch130', 'eil51', 'kroA100', 'pr152']
default_params = {'replacement': 'full_gen_replacement_elitist',
                  'seed': None,
                  'pop_size': None,
                  'gens': None,
                  'mut_p': 0.1,
                  'local_s_iters': 3}

general_data_path = 'results/tsp/'



for instance in all_instances:
    print(instance)
    default_params['NAME'] = instance
    executions_data_path = general_data_path + instance + f'/memetic_{instance}_data.csv'
    avgs_memetic = get_performance_avgs_for_executions(executions_data_path)
    line_memetic = generate_line_from_data(avgs_memetic)

    executions_data_path = general_data_path + instance + f'/standard_{instance}_data.csv'
    avgs_standard = get_performance_avgs_for_executions(executions_data_path)
    line_standard = generate_line_from_data(avgs_standard)

    plot_evolution([line_memetic, line_standard],
                   default_params,
                   general_data_path + instance + '/comparison',
                   ['avg_best_fitness_found_memetic_algo',
                    'avg_best_fitness_found_genetic_algo'],
                   x_label='target_function_executions',
                   x_logscale=True)
