from sys import argv
import numpy as np
from src.utils.input_output import read_file, parse_multiple_ga_execs_results 
from src.utils.plot_functions import box_plot
from src.gen_algo_framework.replacement import all_replacement_funcs


if __name__ == "__main__":
    DATA_DIRECTORY_PATH: str = argv[1]
    if DATA_DIRECTORY_PATH[-1] != '/':
        DATA_DIRECTORY_PATH: str = DATA_DIRECTORY_PATH + '/'
    

    all_data = []
    labels = []
    for replacement in all_replacement_funcs.keys():
        DATA_FILE_PATH: str = DATA_DIRECTORY_PATH + replacement + '.txt'
        multiple_ga_execs_lines = read_file(DATA_FILE_PATH)

        details, exec_data = parse_multiple_ga_execs_results(multiple_ga_execs_lines)
        all_best_found = []
        for best, _ in exec_data:
            all_best_found.append(best)
        all_data.append(all_best_found)
        labels.append(details['replacement'])
    
    box_plot(np.array(all_data).T, labels, DATA_DIRECTORY_PATH + 'boxplot')