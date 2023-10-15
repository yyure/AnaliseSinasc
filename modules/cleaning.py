import pandas as pd
import numpy as np
import doctest
import yaml
import os

import sys
sys.path.append('modules/')

import config


def filter_rows(df: pd.DataFrame, restrictions: dict[str, list]) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base em um conjunto de restrições
    para cada campo a ser verificado. Retorna um DataFrame somente com as linhas
    que satisfazem todas as restrições.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado
    restrictions : dict[str,list]
        Dicionário em que cada chave é uma coluna do DataFrame e o valor é uma
        lista com os valores aceitos para aquela coluna

    Returns
    -------
    pd.DataFrame
        DataFrame somente com as linhas que satisfazem as restrições

    Examples
    --------
    Teste 1: Filtrar por valores

    >>> data = {'Column_1': [1, 1, 2, 2], 'Column_2': ['x', 'y', 'x', 'y']}
    >>> df = pd.DataFrame(data)
    >>> restrictions = {'Column_1': [2], 'Column_2': ['x']}
    >>> filtered_df = filter_rows(df, restrictions)
    >>> filtered_df
       Column_1 Column_2
    2         2        x

    Teste 2: Valores ausentes

    >>> data = {'Column_1': [1.0, np.nan], 'Column_2': ['x', 'x']}
    >>> df = pd.DataFrame(data)
    >>> restrictions = {'Column_1': [1.0], 'Column_2': ['x']}
    >>> filtered_df = filter_rows(df, restrictions)
    >>> filtered_df
       Column_1 Column_2
    0       1.0        x

    Teste 3: DataFrame vazio

    >>> df = pd.DataFrame(columns=['Column_1', 'Column_2'])
    >>> restrictions = {'Column_1': [1, 2], 'Column_2': ['x']}
    >>> filtered_df = filter_rows(df, restrictions)
    >>> filtered_df
    Empty DataFrame
    Columns: [Column_1, Column_2]
    Index: []
    """
    for restriction in restrictions:
        # Nome da coluna e valores aceitos para a coluna
        column = restriction
        subset = restrictions[column]

        try:
            # Encontra as linhas válidas e filtra o DataFrame
            valid_rows = df[column].isin(subset)
            df = df[valid_rows]
        except KeyError:
            print(f"Erro: Coluna {column} não encontrada.")
    
    return df


def filter_by_z_score(df: pd.DataFrame, columns: list[str], limit: float) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base no Z-Score de cada elemento. Retorna um
    DataFrame somente com as linhas em que o Z-Score de cada elemento é menor do que o
    limite, em módulo.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado
    columns : list[str]
        Lista com as colunas a serem consideradas no filtro
    limit : float
        Z-Score máximo para que um elemento seja considerado válido

    Returns
    -------
    pd.DataFrame
       DataFrame somente com as linhas em que o z-score de cada elemento está
       abaixo do limite estabelecido

    Examples
    --------
    Teste 1: Filtra valores

    >>> data = {'Column': [-10, 20, 30, 40, 100]}
    >>> df = pd.DataFrame(data)
    >>> columns = ['Column']
    >>> limit = 1.0
    >>> filtered_df = filter_by_z_score(df, columns, limit)
    >>> filtered_df
       Column
    1      20
    2      30
    3      40
    """
    try:
        # Média e desvio padrão das colunas
        mean = df.mean()
        std_dev = df.std()
    except TypeError:
        print("Erro: todos os valores devem ser numéricos.")
        return pd.DataFrame()

    # DataFrame com o Z-Score de cada elemento em relação à coluna
    z_scores = (mean - df) / std_dev
    # Se algum elemento está como NaN, então seu Z-Score é zero
    z_scores.fillna(0, inplace=True)
    
    for column in columns:
        try:
            # Filtra o DataFrame com as linhas cujo Z-Score é menor do que o limite
            valid_rows = df.loc[abs(z_scores[column]) < limit]
            df = valid_rows
        except KeyError:
            print(f"Erro: Coluna {column} não encontrada.")

    return df


def fill_columns(df: pd.DataFrame, columns_values: dict[str, int]) -> pd.DataFrame:
    """Preenche as linhas vazias de um DataFrame usando valores específicos para cada coluna.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser preenchido
    columns_values : dict[str, int]
        Dicionário em que as chaves são os nomes das colunas e os valores são os que
        preencherão as linhas vazias da coluna

    Returns
    -------
    pd.DataFrame
        DataFrame com as linhas preenchidas
    
    Examples
    --------
    Teste 1: Preenche linha vazia

    >>> data = {'Column': [1.0, 2.0, np.NaN]}
    >>> df = pd.DataFrame(data)
    >>> columns_values = {'Column': 3}
    >>> filled_df = fill_columns(df, columns_values)
    >>> filled_df
       Column
    0     1.0
    1     2.0
    2     3.0
    """
    for column in columns_values:
        value = columns_values[column]

        try:
            # Preenche a coluna com o valor padrão passado
            df[column] = df[column].fillna(value)
        except KeyError:
            print(f"Erro: coluna {column} não encontrada.")

    return df


def load_data(path_input: str, path_output: str):
    """Função que recebe o arquivo com o conjunto de dados brutos e gera
    um arquivo com os dados tratados. Todos os dados no arquivo de saída
    são do tipo np.int32

    Parameters
    ----------
    path_input : str
        Endereço do arquivo com os dados brutos
    path_output : str
        Endereço em que será criado o arquivo com os dados tratados
    
    Returns
    -------
    None
    """
    # Verifica se o arquivo de configuração existe, caso contrário gera o arquivo
    config_file_path = 'data/config.yaml'
    if not os.path.exists(config_file_path):
        config.generate_config_file(config_file_path)

    # Carrega os dados do arquivo de configuração
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    df_index = config_data['df_index']
    columns_to_remove = config_data['columns_to_remove']
    restrictions = config_data['restrictions']
    columns_to_dropna = config_data['columns_to_dropna']
    columns_to_fill_mean = config_data['columns_to_fill_mean']
    columns_to_fill_values = config_data['columns_to_fill_values']
    columns_to_filter_by_z_score = config_data['columns_to_filter_by_z_score']
    z_score_limit = config_data['z_score_limit']
    
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return

    for chunk in df:
        try:
            chunk.set_index(df_index, inplace=True)
        except KeyError:
            print(f"Erro: coluna {df_index} não encontrada.")

        chunk.drop_duplicates(inplace=True)

        # Remove as colunas que não serão utilizadas
        chunk.drop(columns=columns_to_remove, inplace=True, errors="ignore")

        try:
            chunk.dropna(subset=columns_to_dropna, inplace=True)
        except KeyError:
            print(f"Erro: conjunto de colunas {columns_to_dropna} inválido")

        try:
            # Preenche as linhas vazias, trocando pela média dos valores
            columns_mean = chunk[columns_to_fill_mean].mean()
            chunk[columns_to_fill_mean] = chunk[columns_to_fill_mean].fillna(columns_mean)
        except KeyError:
            print(f"Erro: conjunto de colunas {columns_to_fill_mean} inválido")

        chunk.dropna(inplace=True)

        try:
            # Converte o tipo de dados do DataFrame
            chunk = chunk.astype(np.int32)
        except (ValueError, TypeError):
            print("Erro: todos os valores devem ser inteiros")
        
        # Remove as linhas em que as colunas categóricas estão com algum valor não aceito
        chunk = filter_rows(chunk, restrictions)

        # Preenche as colunas com valores padrão especificados
        chunk = fill_columns(chunk, columns_to_fill_values)

        # Remove as linhas que possuem possíveis outliers em alguma coluna
        chunk = filter_by_z_score(chunk, columns_to_filter_by_z_score, z_score_limit)

        # Salva o DataFrame no arquivo de saída
        if not os.path.exists(path_output):
            chunk.to_csv(path_output, mode='w', sep=';')
        else:
            chunk.to_csv(path_output, mode='a', header=False, sep=';')


if __name__ == "__main__":
    doctest.testmod(verbose=True)