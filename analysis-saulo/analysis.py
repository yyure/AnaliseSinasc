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

def read_and_filter_csv(file_path: str, columns_to_keep: List[str]) -> pd.DataFrame:
    """Lê um arquivo CSV e retorna um DataFrame com apenas as colunas especificadas.

    Parameters
    ----------
    file_path : str
        O caminho do arquivo CSV a ser lido.
    columns_to_keep : List[str]
        Uma lista das colunas a serem mantidas no DataFrame resultante.

    Returns
    -------
    DataFrame
        Um DataFrame contendo apenas as colunas especificadas.
    """
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(file_path, encoding="unicode_escape", engine="python", sep=";")

        # Filtra o DataFrame para manter apenas as colunas que existem no arquivo
        columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df = df[columns_to_keep]

        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {str(e)}")
        return None
    
if __name__ == "__main__":
    doctest.testmod()