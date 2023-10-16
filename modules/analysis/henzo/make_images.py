import sys

import analysis


sys.path.append('../../../')
path_input = 'data/dados.csv'

analysis.analise_peso(path_input)
analysis.analise_apgar_raca(path_input)
analysis.analise_filmort_raca(path_input)