

from src.tsp.euclidean_tsp_ga_exec import ga_exec_for_euctsp
from src.utils.input_output import write_line_to_csv_file
from src.utils.others import seed_in_use


all_instances = [('berlin52', 50, 17000),
                 ('ch130', 55, 100000),
                 ('eil51', 55, 14600),
                 ('kroA100', 50, 65000),
                 ('pr152', 55, 140000)]

default_params = {'replacement': 'full_generational_replacement',
                  'seed': None,
                  'pop_size': None,
                  'gens': None,
                  'mut_p': 0.01,
                  'local_s_iters': 0}

general_output_path = 'results/tsp/'
general_instance_path = 'instances/euc_TSP/'


total_execs = 30

for instance, pop_size, n_generations in all_instances:
    seeds = []
    default_params['pop_size'] = pop_size
    default_params['gens'] = n_generations
    for i in range(total_execs):
        curr_instance_path = general_instance_path + instance + '.tsp'
        curr_output_path = general_output_path + instance + '/standard_gr'
        default_params['seed'] = seed_in_use(None)
        seeds.append(default_params['seed'])
        if i  == total_execs - 1:
            ga_exec_for_euctsp(curr_instance_path,
                               curr_output_path,
                               default_params,
                               write_solution=True,
                               write_detailed_evo=True,
                               plot_generational_evo=False,
                               plot_detailed_evo=True,
                               plot_final_solution=True,
                               animate_evo=False,
                               write_execution_time=True)
        else:
            ga_exec_for_euctsp(curr_instance_path,
                               curr_output_path,
                               default_params,
                               write_detailed_evo=True,
                               write_execution_time=True)

    write_line_to_csv_file(general_output_path + instance + '/standard_gr_seeds.csv', seeds, mode='w')

