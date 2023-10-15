import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict
import geopandas as gpd

from data.mapping import return_state, return_region

region_mapping = return_region()
state_mapping = return_state()

def generate_bar(data_dict: Dict[str, pd.DataFrame], column_name: str, x_label: str, title: str, output_path: str):
    """Cria um gráfico de barras para uma coluna específica de um dicionário de DataFrames e salva em um arquivo.

    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Um dicionário onde as chaves são rótulos e os valores são DataFrames.
    column_name : str
        Nome da coluna que você deseja visualizar.
    x_label : str
        Rótulo do eixo x.
    title : str
        Título do gráfico.
    output_path : str
        Caminho do arquivo de saída.

    Returns
    -------
    None
    """
    plt.figure(figsize=(10, 6))

    for label, df in data_dict.items():
        df_copy = df.copy()
        df_copy[column_name] = pd.to_numeric(df_copy[column_name], errors='coerce')
        mean_value = df_copy[column_name].mean()
        
        plt.bar(label, mean_value, color='midnightblue')

    
    plt.xlabel(x_label)
    plt.title(title)
    plt.tight_layout()

    plt.savefig(output_path)

def generate_boxplot(data_dict: Dict[str, pd.DataFrame], column_name: str, x_label: str, title: str, output_path: str, upper_limit=None):
    """Cria um boxplot para uma coluna específica de um dicionário de DataFrames e salva em um arquivo.

    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
         Um dicionário onde as chaves são rótulos e os valores são DataFrames.
    column_name : str
        Nome da coluna que você deseja visualizar.
    x_label : str
        Rótulo do eixo x.
    title : str
        Título do gráfico.
    output_path : str
        Caminho do arquivo de saída.

    Returns
    -------
    None
    """
    plt.figure(figsize=(10, 6))
    
    data = [pd.to_numeric(df[column_name], errors='coerce') for df in data_dict.values()]
    labels = data_dict.keys()

    plt.ylim(0, upper_limit)
    plt.boxplot(data, labels=labels)
    plt.xlabel(x_label)
    plt.title(title)
    plt.tight_layout()

    plt.savefig(output_path)

def generate_heatmap(dataframes_dict: Dict[str, pd.DataFrame], column_name: str, shapefile_path: str, output_path: str):
    """Gera um mapa de calor com a média de uma coluna específica por estado e o salva como uma imagem.

    Parameters
    ----------
    dataframes_dict : Dict[str, pd.DataFrame]
        Um dicionário de DataFrames, onde as chaves são os estados e os valores são DataFrames com os dados.
    column_name : str
        O nome da coluna a ser usada para calcular a média.
    shapefile_path : str
        O caminho para o arquivo Shapefile que contém as geometrias dos estados.
    output_path : str
        O caminho para salvar a imagem do mapa de calor.

    Returns
    -------
    None
    """
    plt.figure(figsize=(10, 6))

    # Carrega o Shapefile
    gdf = gpd.read_file(shapefile_path)

    # Calcula a média e a adiciona para cada estado no dicionário
    state_means = {}
    for state, state_df in dataframes_dict.items():
        state_df.loc[:, column_name] = pd.to_numeric(state_df[column_name], errors='coerce')
        mean = state_df[column_name].mean()
        state_means[state] = mean
    gdf["média"] = gdf["nome"].map(state_means)

    # Cria e slava o mapa de calor
    gdf.plot(column="média", cmap="YlOrRd", linewidth=0.5, edgecolor="0", legend=True)
    plt.title(f"Média de {column_name} por Estado")
    plt.savefig(output_path)