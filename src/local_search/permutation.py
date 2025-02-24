'''Module with functions for local search
with permutations'''

from typing import List, MutableSequence, Tuple


def in_place_reverse_segment(sequence: MutableSequence,
                             start: int,
                             end: int) -> None:
    '''Reverses a segment of a mutable sequence in place.
    This function reverses the order of the elements between
    the given indices, modifying the sequence directly
    without creating a new one.
    Args:
        sequence (MutableSequence): The sequence to be modified.
        start (int): The starting index of the segment to reverse.
        end (int): The ending index of the segment to reverse.
    '''
    assert 0 <= start < len(sequence) and 0 <= end < len(sequence)
    i, j = start, end
    while i < j:
        sequence[i], sequence[j] = sequence[j], sequence[i]
        i += 1
        j -= 1


def generate_2_opt_cut_points(sequence_len: int):
    '''
    Generates all possible cut points for the 2-opt neighborhood.

    This function returns a list of tuples representing all pairs
    of indices (i, j) where 1 <= i < j < sequence_len.
    These cut points are used to identify segments to reverse in
    the 2-opt local search.

    Args:
        sequence_len (int): The length of the sequence.

    Returns:
        List[Tuple[int, int]]: A list of tuples containing the cut points.
    '''

    cut_points: List[Tuple] = []
    for i in range(1, sequence_len):
        for j in range(i + 1, sequence_len):
            cut_points.append((i, j))
    return cut_points


def local_search_2_opt(initial_solution: MutableSequence,
                       options: dict,
                       inside_ga_execution: bool = False) -> float:
    '''
    Performs local search to the given solution using the 2-opt neighborhood for TSP.
    Modifies the given solution.
    Args:
        initial_solution (MutableSequence): The initial solution or tour
            (sequence of cities) to improve using the local search.
        options (dict): A dictionary containing the following keys:
            - 'target_f' (Callable[[MutableSequence, dict], float]): The objective
              function that computes the quality (distance) of a tour.
            - 'local_s_iters' (int): The maximum number of iterations to perform
              in the local search.
        inside_ga_execution (bool): Flag to indicate that the function is being used
            inside a genetic algorithm execution.
    Returns:
        float: The fitness of the best tour found during the local search.
    '''
    f = options['target_f']
    iterations = options['local_s_iters']

    x = initial_solution
    best_f_x = f(x, options, inside_ga_execution)
    cut_points = generate_2_opt_cut_points(len(x))

    for _ in range(iterations):
        #iter_best_f_x = best_f_x

        for i, j in cut_points: # iterating through neighborhood

            in_place_reverse_segment(x, i, j) # compute neighbor using x
            f_neighbor_x = f(x, options, inside_ga_execution)

            if f_neighbor_x < best_f_x:
                best_f_x = f_neighbor_x
            else: # not better neighbor
                in_place_reverse_segment(x, i, j) # recompute x

        #if iter_best_f_x == best_f_x: # local optima
        #    break

    return best_f_x
