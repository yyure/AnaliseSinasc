import pandas as pd
import numpy as np
import yaml
import os
import matplotlib.pyplot as plt
import doctest

import config1
import cleaning


def filter_data_1(path_input: str, path_output: str):

    # Verifica se o arquivo de configuração existe, caso contrário gera o arquivo
    config_file_path = 'config1.yaml'
    if not os.path.exists(config_file_path):
        config1.generate_config_file(config_file_path)

    # Carrega os dados do arquivo de configuração
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    df_index = config_data['df_index']
    columns_to_remove = config_data['columns_to_remove']

    # Abre os dados pré-filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Filtra os dados para esta analise
    for chunk in df:
        try:
            chunk.set_index(df_index, inplace=True)
        except KeyError:
            print(f"Erro: coluna {df_index} não encontrada.")

         # Remove as colunas que não serão utilizadas nesta analise
        chunk.drop(columns=columns_to_remove, inplace=True, errors="ignore")

        # Salva o DataFrame no novo arquivo de saída
        chunk.to_csv(path_output, mode='a', sep=';')

def coleta_dados(path_input: str):

    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    end = pd.DataFrame([])
    for chunk in df:
        chunk = chunk.loc[['RACACOR', 'RACACORMAE']]
        end.add(chunk.value_counts(), fill_value = 0)

    end = end.groupby(level = 0).sum()
    end['RACACOR'] /= end['RACACOR'].sum
    end['RACACORMAE'] /= end['RACACORMAE'].sum

    fig, axs = plt.subplots(1, 2, sharey = True, tight_layout = True)

    axs[0].hist(end['RACACOR'], bins = 5)
    axs[1].hist(end['RACACORMAE'], bins = 5)

    plt.show()

    diff = end['RACACORMAE'] - end['RACACOR']

    plt.hist(diff)
    plt.show()    

if __name__ == "__main__":
    coleta_dados('../data/saida.csv')