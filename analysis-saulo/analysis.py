import pandas as pd
import numpy as np
from typing import Dict, List
from data_analise.mapping import return_region, return_state
import doctest

region_mapping = return_region()
state_mapping = return_state()

def separate_by_location(df: pd.DataFrame, mapping: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """
    Separa os dados do DataFrame em DataFrames individuais para cada estado ou região com base nos códigos de Códigos de Municípios do IBGE.

    Parâmetros:
    - df: DataFrame
        O DataFrame a ser analisado.
    - mapping: dict
        Um dicionário onde as chaves são os códigos dos estados ou regiões e os valores são as regiões correspondentes.

    Retorna:
    - dict of DataFrames
        Um dicionário onde as chaves são as regiões ou estados e os valores são DataFrames correspondentes a cada região.

    Exemplos:

    Teste 1: usando state_mapping

    >>> df = pd.DataFrame({'CODMUNNASC': ['12', '27', '53'], 'Column': [10, 20, 30]})
    >>> state_mapping = {"12": 'Acre', "27": 'Alagoas', "32": 'Espírito Santo'}
    >>> separate_by_location(df, state_mapping)
    {'Acre':   CODMUNNASC  Column
    0         12      10, 'Alagoas':   CODMUNNASC  Column
    1         27      20, 'Espírito Santo': Empty DataFrame
    Columns: [CODMUNNASC, Column]
    Index: []}

    
    Teste 2: usando region_mapping

    >>> df = pd.DataFrame({'CODMUNNASC': ['1', '2'], 'Column': [10, 20]})
    >>> region_mapping = {"1": 'Norte', "2": 'Nordeste'}
    >>> separate_by_location(df, region_mapping)
    {'Norte':   CODMUNNASC  Column
    0          1      10, 'Nordeste':   CODMUNNASC  Column
    1          2      20}
    """
    
    # Verifica se o mapeamento atual (mapping) é para estados (state_mapping) ou regiões (region_mapping).
    # Dependendo do mapeamento, a coluna "CODMUNNASC" é ajustada para conter os códigos apropriados.
    if mapping == state_mapping:
        df["CODMUNNASC"] = df["CODMUNNASC"].str[:2]
    elif mapping == region_mapping:
        df["CODMUNNASC"] = df["CODMUNNASC"].str[:1]

    region_data = {}

    for code, region in mapping.items():
        # Filtra o DataFrame original (df) com base no código da região atual (code).
        region_df = df[df["CODMUNNASC"] == code]
        region_data[region] = region_df
    
    return region_data
    
def calculate_and_save_region_averages(data_dict: Dict[str, pd.DataFrame], column_name: str, output_path: str):
    """Função gera um arquivo .csv com as médias da coluna por região.

    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Um dicionário de DataFrames, onde as chaves são os estados e os valores são DataFrames com os dados.
    column_name : str
        Coluna a ser analisada.
    output_path : str
        O caminho para salvar o arquivo .csv.
    """
    # Inicia listas vazias
    labels = []
    medias = []
    somas = []

    for label, df in data_dict.items():
        df_copy = df.copy()
        df_copy[column_name] = pd.to_numeric(df_copy[column_name], errors='coerce')

        # Calcula a soma e a média
        col_sum = df_copy[column_name].sum()
        col_mean = df_copy[column_name].mean()

        # Adiciona os resultados às listas
        labels.append(label)
        somas.append(col_sum)
        medias.append(col_mean)

    # Cria um DataFrame com os resultados
    data = {
        'DataFrame': labels,
        'Soma Total': somas,
        'Média': medias
    }
    summary_df = pd.DataFrame(data)

    summary_df.to_csv(output_path, sep=";", index=False)

if __name__ == '__main__':
    doctest.testmod(verbose=True)