
from statistics import mean, median, stdev
from numpy import ndarray
from src.utils.input_output import read_lines_from_csv_file
from src.utils.plot_functions import box_plot, generate_line_from_data, plot_evolution


def get_results_and_performance_avgs_for_executions(executions_data_path: str) -> ndarray:
    accumulated_sum = None
    number_executions = 0
    results = []
    for single_exec in read_lines_from_csv_file(executions_data_path):
        results.append(single_exec[-1])
        number_executions += 1
        if accumulated_sum is None:
            accumulated_sum = single_exec
        else:
            accumulated_sum += single_exec

    return accumulated_sum / number_executions, results # pyright: ignore


def calculate_statistics(data):
    return {
        'Best': min(data),
        'Worst': max(data),
        'Mean': mean(data),
        'Median': median(data),
        'Standard Deviation': stdev(data) if len(data) > 1 else 0
    }


all_instances = ['berlin52', 'ch130', 'eil51', 'kroA100', 'pr152']
default_params = {'replacement': None,
                  'seed': None,
                  'pop_size': None,
                  'gens': None,
                  'mut_p': None,
                  'local_s_iters': None}

general_data_path = 'results/tsp/'


all_algorithms = ['memetic', 'standard', 'standard_gr', 'standard_rw']

box_plot_labels = ['memetic', 'GA-gre', 'GA-gr', 'GA-rw']


for instance in all_instances:
    print('\n------------------------------------------------------------------------------')
    print(instance)
    default_params['NAME'] = instance

    lines = []
    all_results = []
    all_times = []

    for algo in all_algorithms:
        executions_data_path = general_data_path + instance + f'/{algo}_{instance}_data.csv'
        avgs, results = get_results_and_performance_avgs_for_executions(executions_data_path)
        lines.append(generate_line_from_data(avgs))
        all_results.append(results)
        print(f'statistics - {instance}-{algo}:', calculate_statistics(results))
        best_f_iter_num, best_f = min(enumerate(results), key=lambda x: x[1])
        print(f'best found - {algo}:', best_f_iter_num, best_f)
        for line in read_lines_from_csv_file(general_data_path + instance + f'/{algo}_seeds.csv'):
            print('seed:', int(line[best_f_iter_num]), '\n')

        times = []
        for time_exec in read_lines_from_csv_file(general_data_path + instance + f'/{algo}_{instance}_execution_time.csv'):
            times.append(time_exec[0])

        print(f'TIME statistics - {instance}-{algo}:', calculate_statistics(times))
        all_times.append(times)


    plot_evolution(lines,
                   default_params,
                   general_data_path + instance + '/comparison',
                   ['avg_best_memetic_algo',
                    'avg_best_GA_gen_replacement_elitism',
                    'avg_best_GA_gen_replacement',
                    'avg_best_GA_replacement_worst'],
                   x_label='target_function_executions',
                   x_logscale=True)

    box_plot(all_results, box_plot_labels, general_data_path + instance +'/boxplot.png', True)
    box_plot(all_times, box_plot_labels, general_data_path + instance +'/boxplot_times.png', y_logscale=False, y_label='Time(seconds)')
