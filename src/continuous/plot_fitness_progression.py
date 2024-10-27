from sys import argv
from src.utils.input_output import read_file, parse_multiple_ga_executions_data
from src.utils.others import compute_generational_avgs
from src.utils.plot_functions import generate_line_from_data, plot_evolution
from src.gen_algo_framework.replacement import all_replacement_funcs


if __name__ == "__main__":
    DATA_DIRECTORY_PATH: str = argv[1]
    if DATA_DIRECTORY_PATH[-1] != '/':
        DATA_DIRECTORY_PATH: str = DATA_DIRECTORY_PATH + '/'

    all_lines_of_avg_of_best_found = []
    all_labels_of_best_f = []
    const = '_avg_best_fitness_found'

    for replacement in all_replacement_funcs.keys():
        DATA_FILE_PATH: str = DATA_DIRECTORY_PATH + replacement + '.txt'
        multiple_ga_execs_lines = read_file(DATA_FILE_PATH)

        details, data = parse_multiple_ga_executions_data(multiple_ga_execs_lines)

        gen_avgs = compute_generational_avgs(data)

        avg_best_f_line = generate_line_from_data(gen_avgs[0])
        avg_avg_f_line = generate_line_from_data(gen_avgs[1])
        labels = ['avg_best_fitness_found', 'avg_avg_population_fitnes']

        lines = [avg_best_f_line, avg_avg_f_line]
        plot_evolution(lines, details, DATA_DIRECTORY_PATH + replacement, labels)

        all_lines_of_avg_of_best_found.append(avg_best_f_line)
        all_labels_of_best_f.append(replacement + const)

    details['replacement'] = None
    plot_evolution(all_lines_of_avg_of_best_found, details, DATA_DIRECTORY_PATH + 'comparison', all_labels_of_best_f)