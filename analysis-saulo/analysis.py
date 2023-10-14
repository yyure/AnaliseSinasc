import pandas as pd
import numpy as np
from typing import Dict, List
from data_analise.mapping import return_region, return_state

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

def read_and_filter_csv(file_path: str, columns_to_keep: List[str]):
    """
    Lê um arquivo CSV e retorna um DataFrame com apenas as colunas especificadas.

    Parâmetros:
    - file_path (str): O caminho do arquivo CSV a ser lido.
    - columns_to_keep (list): Uma lista das colunas a serem mantidas no DataFrame resultante.

    Retorna:
    - DataFrame: Um DataFrame contendo apenas as colunas especificadas.
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

def calculate_and_print_stats(dataframes_dict: Dict[str, pd.DataFrame]):
    """
    Calcula e imprime a média, mediana e desvio padrão de todas as colunas em todos os DataFrames de regiões.
    Realiza a conversão para valores numéricos antes do cálculo.

    Parâmetros:
    - dataframes_dict (dict): Um dicionário de DataFrames para cada região.
    """
    for region, dataframe in dataframes_dict.items():
        print(f"Estatísticas para a região '{region}':")
        for column_name in dataframe.columns:
            column = pd.to_numeric(dataframe[column_name], errors='coerce')
            print("Coluna: ", column_name)
            print("Média: ", column.mean())
            print("Mediana: ", column.median())
            print("Desvio Padrão: ", column.std())
            print("#"*40)



if __name__ == "__main__":
    df = read_and_filter_csv("../data/saida.csv", ["CODMUNNASC", "QTDFILVIVO", "QTDFILMORT", "GESTACAO", "PARTO", "APGAR1", "APGAR5",
                                                   "SERIESCMAE", "QTDPARTNOR", "QTDPARTCES", "CONSPRENAT", "MESPRENAT", "KOTELCHUCK"])

    df_region = separate_by_location(df, region_mapping)
    calculate_and_print_stats(df_region)


