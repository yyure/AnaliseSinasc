import pandas as pd
import numpy as np
import yaml
import os
import matplotlib.pyplot as plt
import doctest

import config1
import cleaning

def analise_1_0(path_input: str):

    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = [1, 2, 3, 4, 5], columns = ['RACACOR', 'RACACORMAE'])
    data_set.fillna(0, inplace=True)

    # Índice usado na iteração
    RACACOR_index = ['1', '2', '3', '4', '5']

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACOR', 'RACACORMAE']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACOR\' ou \'RACACORMAE\'.')
            return data_set
        
        # Itera sobre as cores
        for COR in RACACOR_index:
            filtro = chunk['RACACOR'] == COR
            count_cor_filho = len(chunk.loc[filtro])

            filtro = (chunk['RACACORMAE'] == COR)
            count_cor_mae = len(chunk.loc[filtro])

            data_set.loc[int(COR), 'RACACOR'] += count_cor_filho
            data_set.loc[int(COR), 'RACACORMAE'] += count_cor_mae

    # Normaliza os valores percentualmente
    data_set.iloc[:, :] = data_set.iloc[:, :].apply(lambda x: x/x.sum(), axis=0)

    #Plota os gráficos lado a lado
    fig, axs = plt.subplots(1, 2, sharey = True, tight_layout = True)
    X_label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena']
    cores = ['tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red']

    axs[0].set_ylabel('Frequência')
    axs[0].set_title('Cor do bebê')
    axs[1].set_title('Cor da mãe')

    axs[0].bar(X_label, data_set['RACACOR'])
    axs[1].bar(X_label, data_set['RACACORMAE'], color=cores)

    plt.show()

    #Plota a diferença de cor da mãe e do filho
    diff = data_set['RACACORMAE'] - data_set['RACACOR']
    
    fig, axs = plt.subplots()
    axs.set_title('Porcentagem da diferença de cores')
    axs.bar(X_label, diff*100)
    
    plt.show()    

def analise_1_2(path_input: str):
    
    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = [1, 2, 3, 4, 5], columns = ['RACACOR', 'RACACORMAE'])
    data_set.fillna(0, inplace=True)

    # Índice usado na iteração
    RACACOR_index = ['1', '2', '3', '4', '5']

    # Itera sobre os chunks
    

if __name__ == "__main__":
    analise_1_0('../data/saida.csv')