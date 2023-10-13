import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

def plot_bar(data_dict: Dict[str, pd.DataFrame], column_name: str, x_label: str, y_label: str, title: str, output_path: str) -> None:
    """
    Cria um gráfico de barras para uma coluna específica de um dicionário de DataFrames e salva em um arquivo.

    Parâmetros:
    - data_dict (dict): Um dicionário onde as chaves são rótulos e os valores são DataFrames.
    - column_name (str): Nome da coluna que você deseja visualizar.
    - x_label (str): Rótulo do eixo x.
    - y_label (str): Rótulo do eixo y (deve descrever a variável).
    - title (str): Título do gráfico.
    - output_path (str): Caminho do arquivo de saída.
    """
    plt.figure(figsize=(10, 6))

    for label, df in data_dict.items():
        df_copy = df.copy()
        df_copy[column_name] = pd.to_numeric(df_copy[column_name], errors='coerce')
        plt.bar(label, df_copy[column_name].mean(), label=label)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path)

def plot_boxplot(data_dict: Dict[str, pd.DataFrame], column_name: str, x_label: str, y_label: str, title: str, output_path: str) -> None:
    """
    Cria um boxplot para uma coluna específica de um dicionário de DataFrames e salva em um arquivo.

    Parâmetros:
    - data_dict (dict): Um dicionário onde as chaves são rótulos e os valores são DataFrames.
    - column_name (str): Nome da coluna que você deseja visualizar.
    - x_label (str): Rótulo do eixo x.
    - y_label (str): Rótulo do eixo y (deve descrever a variável).
    - title (str): Título do gráfico.
    - output_path (str): Caminho do arquivo de saída.
    """
    plt.figure(figsize=(10, 6))
    
    data = [pd.to_numeric(df[column_name], errors='coerce') for df in data_dict.values()]
    labels = data_dict.keys()

    plt.boxplot(data, labels=labels)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()

    plt.savefig(output_path)