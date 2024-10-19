from sys import argv
from src.utils.input_output import read_file, parse_multiple_ga_executions_data
from src.utils.others import compute_generational_avgs
from src.utils.plot_functions import generate_line_from_data, plot_evolution

if __name__ == "__main__":
    DATA_FILE_PATH: str = argv[1]
    OUTPUT_FILE_PATH: str = argv[2]
    multiple_ga_execs_data = read_file(DATA_FILE_PATH)
    details, data = parse_multiple_ga_executions_data(multiple_ga_execs_data) 
    print(len(data))

    gen_avgs = compute_generational_avgs(data)
    print(len(gen_avgs))


    avg_best_f_line = generate_line_from_data(gen_avgs[0])
    avg_avg_f_line = generate_line_from_data(gen_avgs[1])
    labels = ['avg_best_fitness_found', 'avg_avg_population_fitnes']

    lines = [avg_best_f_line, avg_avg_f_line]
    plot_evolution(lines, details, OUTPUT_FILE_PATH, labels)