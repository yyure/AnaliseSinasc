import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_bar_chart_with_hline(values: list[int], labels: list[str], path_output: str, line_y: float = 0,
    bottom: float = 0, title: str = '', x_label: str = '', y_label: str = '', line_label: str = '', 
    hline: bool = True):
    """Cria um gráfico de barras com uma linha horizontal e salva em um arquivo.

    Parameters
    ----------
    values : list[int]
        Lista com os valores das barras
    labels : list[str]
        Lista com os rótulos das barras
    line_y : float
        Coordenada horizontal da linha
    path_output : str
        Arquivo em que o gráfico será salvo
    bottom : float, optional
        Valor inicial do eixo vertical, by default 0
    title : str, optional
        Título do gráfico, by default ''
    x_label : str, optional
        Legenda do eixo horizontal, by default ''
    y_label : str, optional
        Legenda do eixo vertical, by default ''
    line_label : str, optional
        Legenda da linha horizontal, by default ''
    hline : bool, optional
        Se True, gera o gráfico com a linha horizontal, by default True
    
    Returns
    -------
    None
    """
    bar_values = values - bottom

    fig, ax = plt.subplots()

    bar_width = 0.4
    index = np.arange(len(values))

    ax.bar(index, bar_values, bar_width, bottom=bottom, color='#003f5c')

    if hline:
        ax.axhline(y=line_y, color='black', linestyle='--', label=line_label)
        ax.legend()

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(index)
    ax.set_xticklabels(labels)

    plt.savefig(path_output)


def plot_stacked_percentage_hbar(data: pd.DataFrame, column_1: str, column_2: str, labels_bars: list[str],
    path_output: str, label_subbar_1: str = '', label_subbar_2: str = '', title: str = ''):
    """Cria um gráfico de barras empilhadas a partir de duas colunas de um DataFrame,
    onde o comprimento de cada barra é relativo à sua frequência na coluna, em porcentagem.
    O gráfico é salvo em um arquivo.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame com as colunas que serão usadas
    column_1 : str
        Primeira coluna
    column_2 : str
        Segunda coluna
    labels_bars : list[str]
        Rótulos das barras
    path_output : str
        Arquivo em que o gráfico será salvo
    label_subbar_1 : str, optional
        Rótulo da primeira coluna, by default ''
    label_subbar_2 : str, optional
        Rótulo da segunda coluna, by default ''
    title : str, optional
        Título do gráfico, by default ''
    
    Returns
    -------
    None
    """
    fig, ax = plt.subplots()

    total = data[column_1] + data[column_2]
    bar_values_1 = data[column_1] / total
    bar_values_2 = data[column_2] / total

    ax.barh(labels_bars, bar_values_1, color='#003f5c', label=label_subbar_1)
    ax.barh(labels_bars, bar_values_2, left=bar_values_1, color='#ffa600', label=label_subbar_2)

    ax.set_title(title)
    ax.legend()

    plt.gca().invert_yaxis()

    plt.savefig(path_output)
