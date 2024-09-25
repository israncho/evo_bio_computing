
from src.utils.input_output import parse_tsp_data, read_file


def test_read_and_parse():
    berlin52 = parse_tsp_data(read_file('instances/euc_TSP/berlin52.tsp'))
    assert berlin52['NAME'] == 'berlin52'
    assert berlin52['TYPE'] == 'TSP'
    assert berlin52['COMMENT'] == '52 locations in Berlin (Groetschel)'
    assert berlin52['DIMENSION'] == 52
    assert berlin52['DIMENSION'] == len(berlin52['rest_of_cities']) + 1
    assert berlin52['EDGE_WEIGHT_TYPE'] == 'EUC_2D'
    assert berlin52['fst_city'] == (565.0, 575.0)
    assert berlin52['ids'][(565.0, 575.0)] == 1
    cities = berlin52['rest_of_cities'].copy()

    curr_id = 2
    for city in cities:
        assert berlin52['ids'][city] == curr_id
        curr_id += 1
