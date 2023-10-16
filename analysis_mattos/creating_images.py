import pandas as pd
import numpy as np
import statics
import matplotlib.pyplot as plt

estados = [
"AC",
"AL",
"AP",
"AM",
"BA",
"CE",
"DF",
"ES",
"GO",
"MA",
"MT",
"MS",
"MG",
"PA",
"PB",
"PR",
"PE",
"PI",
"RN",
"RS",
"RJ",
"RO",
"RR",
"SC",
"SP",
"SE",
"TO"
]

def graph_desv(campo: str):
    """Cria um gráfico de barras mostrando todos
    os desvios padrões estaduais referente ao
    ``campo`` com uma linha vermelha indicando
    o desvio padrão nacional.

    Parameters
    ----------
    campo : str
        Indica o tipo de dado que se refere os
        desvios estuais (e.g. 'IDADEMAE').
    
    Returns
    -------
    None
    """
    # Obtenção do desvio padrão nacional
    df2 = pd.read_csv('Data_UF/Data_BRASIL.csv', sep=';', engine='python')
    desv_nacional = df2.loc[2, campo]

    y_axis = []
    # Iteração sobre os Estados para obtenção dos desvios estaduais
    for estado in estados:
        df1 = pd.read_csv(f'Data_UF/Data_{estado}.csv', sep=';', engine='python')
        df1.set_index(df1['Unnamed: 0'], inplace=True)
        df1.drop(columns=['Unnamed: 0'], inplace=True)
        y = df1.loc['std',campo]
        y_axis.append(y)

    # Plotagem do gráfico
    data = pd.DataFrame({'col1': estados, 'col2': y_axis})
    data.plot(x='col1', y='col2', kind='bar', label='',width=1, edgecolor='black').get_legend().remove()
    plt.title(f'Desvio padrão - {campo}').set_size(8)
    plt.axhline(y=desv_nacional, linestyle='--', label='média dos std',linewidth = '2.4', color='red')
    plt.savefig(f'images/Desv_{campo}_BR.png')


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
    graph_desv('IDADEMAE')
    graph_desv('CONSPRENAT')
    graph_desv('ESCMAE')
    graph_BR('IDADEMAE', 90)
    graph_BR('CONSPRENAT', 90)
    graph_BR('ESCMAE', 0)
    graph_UF('IDADEMAE', 90, [0, 0.1, 0.2])
    graph_UF('CONSPRENAT', 90, [0, 0.1, 0.2, 0.3])
    graph_UF('ESCMAE', 0, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])