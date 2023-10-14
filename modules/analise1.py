import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import doctest

import config1
import cleaning

# Há diferença percentual entre a cor da mãe e a cor dos filhos?
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
    RACACOR_index = [1, 2, 3, 4, 5]

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACOR', 'RACACORMAE']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACOR\' ou \'RACACORMAE\'.')
            return data_set
        
        # Itera sobre as cores
        for COR in RACACOR_index:
            filtro = (chunk['RACACOR'] == COR)
            count_cor_filho = len(chunk.loc[filtro])

            filtro = (chunk['RACACORMAE'] == COR)
            count_cor_mae = len(chunk.loc[filtro])

            data_set.loc[COR, 'RACACOR'] += count_cor_filho
            data_set.loc[COR, 'RACACORMAE'] += count_cor_mae

    print(data_set)
    # Normaliza os valores percentualmente
    data_set.iloc[:, :] = data_set.iloc[:, :].apply(lambda x: x/x.sum(), axis=0)

    print(data_set)
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

# Há diferença de subpeso ou sobrepeso e a cor da mãe?
def analise_1_1(path_input: str):
    
    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    PESO_index = [0, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 8000]

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = RACACOR_index, columns = PESO_index[:-1])
    data_set.fillna(0, inplace=True)

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACORMAE', 'PESO', 'GESTACAO','APGAR5']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'PESO\' ou \'APGAR5\'.')
            return data_set
    
        # Filtra o chunk por GESTACAO
        filtro = (chunk['GESTACAO'] == 5)
        chunk = chunk[filtro]

        # Itera sobre as cores
        for COR in RACACOR_index:

            # Filtra o chunk por COR
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk[filtro]

            # Divide o PESO em intervalos e soma ao data_set
            temp_df = pd.cut(temp_df['PESO'], PESO_index, right = False, labels = PESO_index[:-1])
            data_set.loc[COR] += temp_df.value_counts().transpose()

    # Adiciona linha com soma de cada coluna
    data_set = pd.concat([data_set, data_set.sum(axis = 0).to_frame().T])

    # Normaliza os valores percentualmente
    data_set.iloc[:, :] = data_set.iloc[:, :].apply(lambda x: x/x.sum(), axis=1)

    # Recria as categorias de colunas: SUBPESO(0, 2000), SAUDAVEL(2000, 4000), SOBREPESO(>4000)
    data_set['SUBPESO'] = data_set[PESO_index[0:3]].sum(axis = 1)
    data_set['SAUDAVEL'] = data_set[PESO_index[3:6]].sum(axis = 1)
    data_set['SOBREPESO'] = data_set[PESO_index[6:-1]].sum(axis = 1)

    data_set.drop(PESO_index[:-1], axis = 1, inplace = True)

    # Plota gráficos
    X_label = ['SUBPESO', 'SAUDAVEL', 'SOBREPESO']
    Label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena', 'Média']
    cores = ['tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red']

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout = True)

    axs[0].set_title('Fração de bebês no subpeso')
    axs[1].set_title('Fração de bebês no sobrepeso')
    axs[0].set_ylabel('Porcentagem')
    
    axs[0].bar(Label, data_set['SUBPESO']*100)
    axs[1].bar(Label, data_set['SOBREPESO']*100, color = cores)

    plt.show()

    # Subtrai de cada RACA a média TOTAL
    data_set.iloc[:-1, :] -= data_set.iloc[5, :]

    fig, axs = plt.subplots()
    axs.set_title('Diferença percentual à média \nde bebês amarelos')
    axs.bar(X_label, data_set.loc[3]*100)

    plt.show()

# Há diferença no indice APGAR e a cor da mãe?
def analise_1_2(path_input: str):
    
    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    APGAR_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = RACACOR_index, columns = APGAR_index)
    data_set.fillna(0, inplace=True)

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['RACACORMAE', 'PESO', 'APGAR5']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'PESO\' ou \'APGAR5\'.')
            return data_set
    
        # Itera sobre as cores
        for COR in RACACOR_index:

            # Filtra o chunk por COR
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk[filtro]

            # Divide o PESO em intervalos e soma ao data_set
            temp_df = pd.cut(temp_df['APGAR5'], 11, right = False, labels = APGAR_index)
            data_set.loc[COR] += temp_df.value_counts().transpose()

    # Adiciona linha com soma de cada coluna
    data_set = pd.concat([data_set, data_set.sum(axis = 0).to_frame().transpose()])

    # Normaliza os valores percentualmente
    data_set.iloc[:, :] = data_set.iloc[:, :].apply(lambda x: x/x.sum(), axis=1)

    # Altera as categorias
    data_set['ALTO'] = data_set.iloc[:, 0:3].sum(axis = 1)
    data_set['MEDIO'] = data_set.iloc[:, 3:8].sum(axis = 1)
    data_set['BAIXO'] = data_set.iloc[:, 8:11].sum(axis = 1)

    data_set.drop(APGAR_index, axis = 1, inplace = True)
    print(data_set)

    # Plota por RACA
    Label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena', 'Media']
    cores1 = ['tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red']
    cores2 = ['tab:green', 'tab:green', 'tab:green', 'tab:green', 'tab:green', 'tab:green']

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout = True)

    axs[0].set_ylabel('Frequência')
    axs[0].set_title('APGAR > 7')
    axs[1].set_title('APGAR < 3')

    axs[0].bar(Label, data_set['ALTO']*100)
    axs[1].bar(Label, data_set['BAIXO']*100, color = cores1)

    plt.show()

# Há diferença na quantidade de filhos mortos por cor da mãe?
def analise_1_3(path_input: str):
    
    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = [1, 2, 3, 4, 5], columns = ['QTDFILMORT', 'TOTAL'])
    data_set.fillna(0, inplace=True)

    # Índice usado na iteração
    RACACOR_index = [1, 2, 3, 4, 5]
    FILMORT = [1, 2, 3, 4, 5, 6, 7, 8]

    Serie = pd.Series([])
    # Itera sobre os chunks
    for chunk in df:

        # Fatia o chunk
        try:
            chunk = chunk[['RACACORMAE', 'QTDFILVIVO', 'QTDFILMORT', 'PARIDADE', 'ESCMAE']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'RACACORMAE\', \'QTDFILVIVO\', \'QTDFILMORT\', \'PARIDADE\' ou \'ESCMAE\'.')
            return data_set

        for COR in RACACOR_index:
            filtro = (chunk['RACACORMAE'] == COR)
            temp_df = chunk.loc[filtro]

            data_set.loc[COR, 'QTDFILMORT'] += temp_df['QTDFILMORT'].sum()
            data_set.loc[COR, 'TOTAL'] += len(temp_df['QTDFILMORT'])

    # Normaliza percentualmente
    data_set['QTDFILMORT'] /= data_set['TOTAL']

    # Plota gráfico
    X_label = ['Branco', 'Preto', 'Amarelo', 'Pardo', 'Indigena']
    fig, axs = plt.subplots()

    axs.set_title('Mulheres que já tiveram \num filho nascido morto')
    axs.set_ylabel('Porcentagem')

    axs.bar(X_label, data_set['QTDFILMORT']*100)
    axs.grid(axis = 'y')
    plt.show()

# Há relação entre PESO e IDADE?
def analise_1_4(path_input: str):
    
    # Abre os dados filtrados
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return
    
    # Índice usado na iteração
    IDADE_index = np.arange(10, 61).tolist()
    PESO_index = np.arange(0, 5002).tolist()

    # Dataframe que contará as frequências
    data_set = pd.DataFrame(data = None, index = IDADE_index, columns = PESO_index[:-1])
    data_set.fillna(0, inplace=True)

    # Itera sobre os chunks
    for chunk in df:

        try:
            chunk = chunk[['PESO', 'GESTACAO', 'IDADEMAE']]
        except KeyError:
            print('Erro: arquivo não possui colunas \'PESO\', \'GESTACAO\' ou \'IDADEMAE\'.')
            return data_set

        # Itera sobre as idades
        for IDADE in IDADE_index:
            # Filtra o chunk por COR
            filtro = (chunk['IDADEMAE'] == IDADE)
            temp_df = chunk[filtro]

            # Soma o PESO ao data_set
            temp_df = pd.cut(temp_df['PESO'], PESO_index, right = False, labels = PESO_index[:-1])
            data_set.loc[IDADE] += temp_df.value_counts().transpose()

    fig, axs = plt.subplots()

    axs.imshow(data_set)
    axs.set_xticks(np.arange(len(data_set.index)), labels = data_set.index)
    axs.set_yticks(np.arange(len(data_set.colums)), labels = data_set.columns)

    axs.set_title('PESO por IDADE')
    fig.tight_layout()
    plt.show()

    fig, axs = plt.subplots()

    for IDADE in IDADE_index:
        filtro = data_set.loc[IDADE].apply(lambda x: x > 0)
        ys_coordenada = data_set.columns[filtro]
        xs_coordenada = np.ones(len(ys_coordenada)) * IDADE
        plt.scatter(xs_coordenada, ys_coordenada)

    plt.show()

if __name__ == "__main__":
    analise_1_4('../data/saida.csv')