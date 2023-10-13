import pandas as pd
import numpy as np
from typing import Dict

state_mapping = {
    "12": 'Acre',
    "27": 'Alagoas',
    "16": 'Amapá',
    "13": 'Amazonas',
    "29": 'Bahia',
    "23": 'Ceará',
    "53": 'Distrito Federal',
    "32": 'Espírito Santo',
    "52": 'Goiás',
    "21": 'Maranhão',
    "51": 'Mato Grosso',
    "50": 'Mato Grosso do Sul',
    "31": 'Minas Gerais',
    "15": 'Pará',
    "25": 'Paraíba',
    "41": 'Paraná',
    "26": 'Pernambuco',
    "22": 'Piauí',
    "24": 'Rio Grande do Norte',
    "43": 'Rio Grande do Sul',
    "33": 'Rio de Janeiro',
    "11": 'Rondônia',
    "14": 'Roraima',
    "42": 'Santa Catarina',
    "35": 'São Paulo',
    "28": 'Sergipe',
    "17": 'Tocantins'
}
region_mapping = {
    "1": "Norte",
    "2": "Nordeste",
    "3": "Sudeste",
    "4": "Sul",
    "5": "Centro-Oeste"
}

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