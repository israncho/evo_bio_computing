from src.continuous.multiple_ga_execs import multiple_ga_execs
from src.gen_algo_framework.replacement import all_replacement_funcs

funcs_to_test = [('sphere', (-5.12, 5.12)),
                 ('ackley', (-30.0, 30.0)),
                 ('griewank', (-600.0, 600.0)),
                 ('rastrigin', (-5.12, 5.12)),
                 ('rosenbrock', (-2.048, 2.048))]


params = {'seed': None,
          'f': None,
          'dim': 10,
          'n_bits': 16,
          'interval': None,
          'replacement': None,
          'reps': 50,
          'pop_size': 600,
          'gens': 200,
          'crossover_n_p': 3,
          'mutation_p': 0.1}

for f, interval in funcs_to_test:
    for replacement in all_replacement_funcs.keys():
        params['f'] = f
        params['interval'] = interval
        params['replacement'] = replacement
        multiple_ga_execs(params, f'results/{f}/{replacement}.txt')