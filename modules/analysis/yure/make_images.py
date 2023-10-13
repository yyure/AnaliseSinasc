import analysis, visualization
import sys

sys.path.append('../../..')

dados_csv = 'data/dados.csv'

dados = analysis.dados_racacormae_consprenat(dados_csv)
medias = dados['NUMCONSULTAS'] / dados['NUMREGISTROS']
media_nacional = dados['NUMCONSULTAS'].sum() / dados['NUMREGISTROS'].sum()
visualization.plot_bar_chart_with_hline(values=medias, labels=['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
    bottom = 5, title='Média de consultas de pré-natal por raça/cor da mãe', x_label='', y_label='Média de consultas',
    line_y=media_nacional, line_label='Média nacional', path_output='images/imagem1.png')

dados = analysis.dados_racacormae_locnasc(dados_csv)
locnasc_indigenas = dados.loc[5]['NUMREGISTROS']
visualization.plot_pie_chart(data=locnasc_indigenas, colors=['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'],
    labels=['Hospital', 'Outros estab. de saúde', 'Domicílio', 'Outros', 'Aldeia Indígena'], start_angle=30,
    title='Local de nascimento de bebês de mães indígenas', legend_title='Local de nascimento',
    loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), path_output='images/imagem2.png')

dados = analysis.dados_racacormae_parto(dados_csv)
visualization.plot_stacked_percentage_hbar(data=dados, labels_bars=['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
    column_1='QTDPARTNOR', column_2='QTDPARTCES', label_subbar_1='Partos normais', label_subbar_2='Partos cesários',
    title='Porcentagem de tipos de parto por raça/cor da mãe', path_output='images/imagem3.png')