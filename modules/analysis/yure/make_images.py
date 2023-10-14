import pandas as pd
import numpy as np
import analysis, visualization
import sys

sys.path.append('../../..')

dados_csv = 'data/dados.csv'

dados = analysis.dados_racacormae_consprenat(dados_csv)
media_nacional = np.round(dados['NUMCONSULTAS'].sum() / dados['NUMREGISTROS'].sum(), decimals=2)
visualization.plot_bar_chart_with_hline(values=dados['MEDIA'], labels=['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
    bottom = 5, title='Média de consultas de pré-natal por raça/cor da mãe', x_label='', y_label='Média de consultas',
    line_y=media_nacional, line_label='Média nacional', path_output='images/imagem1.png')

dados = analysis.dados_racacormae_locnasc(dados_csv)
locnasc_indigenas = dados.loc[5]['NUMREGISTROS']
locnasc_indigenas = locnasc_indigenas.sort_values(ascending=False)
visualization.plot_bar_chart_with_hline(values=locnasc_indigenas, labels=['Hospital', 'Domicílio', 'Outros',
    'Aldeia', 'Outros estab.'], bottom=0, title='Local de nascimento de bebês de mães indígenas',
    hline = False, line_y=0, path_output='images/imagem2.png')

dados = analysis.dados_racacormae_parto(dados_csv)
visualization.plot_stacked_percentage_hbar(data=dados, labels_bars=['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
    column_1='QTDPARTNOR', column_2='QTDPARTCES', label_subbar_1='Partos normais', label_subbar_2='Partos cesários',
    title='Porcentagem de tipos de parto por raça/cor da mãe', path_output='images/imagem3.png')