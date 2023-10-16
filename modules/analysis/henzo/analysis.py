"""
Módulo de Análise de Dados e Visualização de Dados

Este módulo contém funções para análise de dados de saúde materna e infantil.

Funcionalidades:
- Analisa os dados de peso dos bebês, cria um histograma e o salva.
- Analisa os dados do índice APGAR por raça, cria um gráfico e o salva.
- Analisa a quantidade de filhos mortos por raça, cria um gráfico e o salva.
- Analisa o peso do bebê em relação à idade da mãe, cria um gráfico de dispersão e o salva.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import doctest

def analise_peso(path_input: str):
    """ Trabalha com os dados limpos e plota o histograma PESO, salvando-o em ./images/.

    Parameters
    ----------
    path_input : str
        Caminho dos dados SISNASC já limpos anteriormente.

    Returns
    -------
    None

    Examples
    --------
    >>> analise_peso('data/dados.csv')
    """

    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    PESO_index = [0] + np.arange(1000, 7101, 100).tolist()

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = RACACOR_index, columns = PESO_index[:-1])
    data_set.fillna(0, inplace=True)
    
    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACORMAE', 'PESO', 'GESTACAO']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'PESO\' ou \'GESTACAO\'.')
            return data_set
    
        # Filtra o chunk apenas quando a GESTACAO está entre 39 e 41 semanas
        filtro = (chunk['GESTACAO'] == 5)
        chunk = chunk[filtro]

        # Itera sobre as cores
        for COR in RACACOR_index:

            # Filtra o chunk por COR
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk[filtro]

            # Divide o PESO em intervalos e soma ao data_set
            temp_df = pd.cut(temp_df['PESO'], PESO_index, right = False, labels = PESO_index[:-1])
            
            data_set.loc[COR] += temp_df.value_counts().transpose()

    # Adiciona linha com soma de cada coluna
    data_set = pd.concat([data_set, data_set.sum(axis = 0).to_frame().T])

    # Soma casos extremos onde o peso é maior que 6000
    data_set[6000] = data_set.loc[:, 6000:].sum(axis = 1)
    data_set.drop(PESO_index[-11:-1], axis = 1, inplace = True)

    # Plota a distribuição total do PESO
    fig, axs = plt.subplots(tight_layout = True, figsize = (10, 6))

    axs.hist(np.arange(data_set.columns.size), weights = data_set.loc[0, :], bins = data_set.columns.size, density = True, color = '#005377')
    
    axs.set_title('Distribuição do peso dos bebês', fontsize = 15)
    axs.set_ylabel('Porcentagem', fontsize = 14)
    axs.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    label = ['< 1000', '[1500, 1600)', '[2000, 2100)', '[2500, 2600)', '[3000, 3100)', '[3500, 3600)', '[4000, 4100)', '[4500, 4600)', '[5000, 5100)', '[5500, 5600)', '>= 6000']
    axs.set_xticks([0] + np.arange(6, data_set.columns.size, 5).tolist(), labels = label, rotation = 45)
    axs.set_xlabel('Intervalos em gramas', fontsize = 12)

    # Salva a imagem em ./images/
    plt.savefig('images/PMF_PESO.png')

def analise_apgar_raca(path_input: str):
    """ Trabalha com os dados limpos e plota o gráfico APGARxRACA, salvando-a em ./images/.

    Parameters
    ----------
    path_input : str
        Caminho dos dados SISNASC já limpos anteriormente.

    Returns
    -------
    None

    Examples
    --------
    >>> analise_apgar_raca('data/dados.csv')
    """

    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    APGAR_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = RACACOR_index, columns = APGAR_index[:-1])
    data_set.fillna(0, inplace=True)

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACORMAE', 'PESO', 'APGAR5']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'PESO\' ou \'APGAR5\'.')
            return data_set
    
        # Itera sobre as cores
        for COR in RACACOR_index:

            # Filtra o chunk por COR
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk[filtro]

            # Divide o PESO em intervalos e soma ao data_set
            temp_df = pd.cut(temp_df['APGAR5'], APGAR_index, right = False, labels = APGAR_index[:-1])
            data_set.loc[COR] += temp_df.value_counts().transpose()

    # Adiciona linha com soma de cada coluna
    data_set = pd.concat([data_set, data_set.sum(axis = 0).to_frame().transpose()])

    # Normaliza os valores percentualmente
    data_set.iloc[:, :] = data_set.iloc[:, :].apply(lambda x: x/x.sum(), axis=1)

    # Altera as categorias
    data_set['BAIXO'] = data_set.iloc[:, 0:3].sum(axis = 1)
    data_set['MEDIO'] = data_set.iloc[:, 3:8].sum(axis = 1)
    data_set['ALTO'] = data_set.iloc[:, 8:11].sum(axis = 1)

    data_set.drop(APGAR_index[:-1], axis = 1, inplace = True)

    # Plota o gráfico por RACA
    Label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena', 'Media']
    width = 0.4

    fig, axs = plt.subplots(tight_layout = True, figsize = (10, 6))

    axs.set_title('Indice APGAR < 7 por raça', fontsize = 15)
    axs.set_ylabel('Porcentagem', fontsize = 14)
    axs.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))

    axs.bar(Label, data_set['BAIXO']*100, -width, align = 'edge', color = '#710627', label = 'APGAR < 3')
    axs.bar(Label, data_set['MEDIO']*100, width, align = 'edge', color = '#D16666', label = '3 <= APGAR <= 7')

    axs.legend(loc = 'upper left')
    axs.grid(axis = 'y', linestyle = '-',color = 'grey', alpha = 0.25)

    # Salva a imagem em ./images/
    plt.savefig('images/APGARxRACA.png')

def analise_filmort_raca(path_input: str):
    """ Trabalha com os dados limpos e plota o gráfico QTDFILMORTxRACA, salvando-a em ./images/.

    Parameters
    ----------
    path_input : str
        Caminho dos dados SISNASC já limpos anteriormente.

    Returns
    -------
    None
    
    Examples
    --------
    >>> analise_filmort_raca('data/dados.csv')
    """


    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = [1, 2, 3, 4, 5], columns = ['QTDFILMORT', 'TOTAL'])
    data_set.fillna(0, inplace=True)

    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    FILMORT = [1, 2, 3, 4, 5, 6, 7, 8]

    Serie = pd.Series([])
    # Itera sobre os chunks
    for chunk in df:

        # Fatia o chunk
        try:
            chunk = chunk[['RACACORMAE', 'QTDFILVIVO', 'QTDFILMORT']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'QTDFILVIVO\' ou \'QTDFILMORT\'.')
            return data_set

        # Itera filtrando sobre cada COR
        for COR in RACACOR_index:
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk.loc[filtro]

            # Calcula e soma quantas mães já tiveram um filho nascido morto antes
            data_set.loc[COR, 'QTDFILMORT'] += np.count_nonzero(temp_df['QTDFILMORT'], axis = 0)
            data_set.loc[COR, 'TOTAL'] += temp_df['QTDFILMORT'].size

    # Normaliza percentualmente
    data_set['QTDFILMORT'] /= data_set['TOTAL']

    # Plota gráfico
    X_label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena']

    fig, axs = plt.subplots(figsize = (10, 6))

    axs.set_title('A mãe já teve algum filho nascido morto antes?', fontsize = 15)
    axs.set_ylabel('Porcentagem', fontsize = 14)
    axs.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))

    axs.bar(X_label, data_set['QTDFILMORT']*100, color = '#005377', label = 'Sim')
    axs.bar(X_label, (1 - data_set['QTDFILMORT'])*100, color = '#C1C1C1', label = 'Não', bottom = data_set['QTDFILMORT']*100)

    axs.grid(axis = 'y', linestyle = '--',color = 'grey', alpha = 0.25)
    axs.legend(loc = 'upper left')

    # Salva a imagem em ./images/
    plt.savefig('images/FILMORTxRACA.png')

def analise_peso_idade(path_input: str):
    """ Trabalha com os dados limpos e plota o gráfico PESOxIDADE, salvando-a em ./images/.

    Parameters
    ----------
    path_input : str
        Caminho dos dados SISNASC já limpos anteriormente.

    Returns
    -------
    None

    Examples
    --------
    >>> analise_peso_idade('data/dados.csv')
    """

    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    IDADE_index = np.arange(8, 61).tolist()
    PESO_index = np.arange(0, 7001).tolist()

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = IDADE_index, columns = PESO_index[:-1])
    data_set.fillna(0, inplace=True)

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['PESO', 'GESTACAO', 'IDADEMAE']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'PESO\', \'GESTACAO\' ou \'IDADEMAE\'.')
            return data_set

        # Itera sobre as idades
        for IDADE in IDADE_index:
            # Filtra o chunk pela IDADE
            filtro = (chunk['IDADEMAE'] == IDADE)
            temp_df = chunk[filtro]

            # Soma o PESO ao data_set
            temp_df = pd.cut(temp_df['PESO'], PESO_index, right = False, labels = PESO_index[:-1])
            data_set.loc[IDADE] += temp_df.value_counts().transpose()

    fig, axs = plt.subplots(figsize = (10, 6))

    axs.set_title('Peso do bebê pela idade da mãe', fontsize = 15)
    axs.set_ylabel('Peso', fontsize = 14)
    axs.set_xlabel('Idade', fontsize = 12)

    for IDADE in IDADE_index:
        filtro = data_set.loc[IDADE].apply(lambda x: x > 0)

        ys_coordenada = data_set.columns[filtro]
        xs_coordenada = np.ones(len(ys_coordenada)) * IDADE

        plt.scatter(xs_coordenada, ys_coordenada, color = '#60AB9A', alpha = 0.2)

    # Salva a imagem em .images/
    plt.savefig('images/PESOxIDADE.png')

if __name__ == "__main__":
    doctest.testmod(verbose=True)