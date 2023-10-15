import pandas as pd
import numpy as np
import statics
import matplotlib.pyplot as plt

estados = {
"AC": 12,
"AL": 27,
"AP": 16,
"AM": 13,
"BA": 29,
"CE": 23,
"DF": 53,
"ES": 32,
"GO": 52,
"MA": 21,
"MT": 51,
"MS": 50,
"MG": 31,
"PA": 15,
"PB": 25,
"PR": 41,
"PE": 26,
"PI": 22,
"RN": 24,
"RS": 43,
"RJ": 33,
"RO": 11,
"RR": 14,
"SC": 42,
"SP": 35,
"SE": 28,
"TO": 17
}


def graph_BR(campo: str, xlabel_rotate: int):
    """Cria um histograma com a frequência relativa
    nacional concernente ao ``campo`` e salva em
    um arquivo.

    Parameters
    ----------
    campo : str
        Indica o tipo de dado que se refere as
        frequências no histograma (e.g. 'IDADEMAE').
    xlabel_rotate : int
        Valor que indica a rotação da indexação do
        eixo x.
    
    Returns
    -------
    None
    """
    # Leitura dos dados para o gráfico
    df = pd.read_csv(f'Freq_Relativa/FRI{campo.lower()}_BR.csv', sep=';', engine='python')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    # Renomear a coluna para 'BRASIL' e plotar o gráfico correspondente
    df.rename(columns={'freq. relativa': 'BRASIL'}, inplace=True)
    # Plotagem do gráfico
    df.plot(kind='bar', x=campo, y='BRASIL', stacked=True, width=1, edgecolor='black', figsize=(8,6)).get_legend().remove()
    plt.xticks(rotation=xlabel_rotate)
    plt.title(f'Frequência relativa nacional - {campo}')
    plt.savefig(f'images/fri_{campo}_BR.png')

def graph_UF(campo: str, xlabel_rotate: int, y_cofing: list[float]):
    """Cria um conjunto de 27 histogramas relativos
    a cada Estado e ao Distrito Federal concernente
    ao ``campo`` e salva em um arquivo.

    Parameters
    ----------
    campo : str
        Indica o tipo de dado que se refere as
        frequências no histograma (e.g. 'IDADEMAE').
    xlabel_rotate : int
        Valor que indica a rotação da indexação do
        eixo x.
    y_cofing : list[float]
        Lista que contém a indexação do eixo y
        desejada.
    
    Returns
    -------
    None
    """
    # Leitura dos dados para os gráficos
    df = pd.read_csv(f'Freq_Relativa/FRI{campo.lower()}_UF.csv', sep=';', engine='python')
    df.drop(columns=['Unnamed: 0'], inplace=True)
    plt.rcParams['figure.dpi'] = 300
    # Configarão do tamanho da figura
    fig = plt.figure(figsize=(8,6))
    # Título geral
    fig.suptitle(f'Frequência relativa - {campo}', fontsize=12)
    # Iteração sobre os estados
    count = 1
    for estado in estados:
        plt.subplot(4,7,count)
        # Plotando gráfico referente ao estado atual
        df[f'{estado} fri.'].plot(kind='bar', width=1, edgecolor='black').set_xticklabels(df[campo], rotation=xlabel_rotate, fontsize=3)
        # Configuração de título e outras opções
        plt.title(f'{estado}').set_size(8)
        plt.tick_params(axis='y', labelsize=5)
        plt.yticks(y_cofing)
        count +=1
    # Ajustes de posicionamento
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.1, hspace=0.5)
    plt.tight_layout()
    plt.savefig(f'images/fri_{campo}_UF.png')
    
if __name__ == "__main__":
    graph_BR('IDADEMAE', 90)
    graph_BR('CONSPRENAT', 90)
    graph_BR('ESCMAE', 0)
    graph_UF('IDADEMAE', 90, [0, 0.1, 0.2])
    graph_UF('CONSPRENAT', 90, [0, 0.1, 0.2, 0.3])
    graph_UF('ESCMAE', 0, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])