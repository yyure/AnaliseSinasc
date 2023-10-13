import pandas as pd
import numpy as np

estados = {
"AC": 12,
"AL": 27,
"AP": 16,
"AM": 13,
"BA": 29,
"CE": 23,
"DF": 53,
"ES": 32,
"GO": 52,
"MA": 21,
"MT": 51,
"MS": 50,
"MG": 31,
"PA": 15,
"PB": 25,
"PR": 41,
"PE": 26,
"PI": 22,
"RN": 24,
"RS": 43,
"RJ": 33,
"RO": 11,
"RR": 14,
"SC": 42,
"SP": 35,
"SE": 28,
"TO": 17
}

def media(df, campo, columns):
    '''
    Dada uma coluna referente a etinia e uma lista referente a quantidades númericas,
    retorna um DataFrame com a média de cada coluna de 'columns' com base no 'campo'.
    '''
    # Criando DataFrame com a coluna incicial
    etnia = ['Branca', 'Preta', 'Amarela', 'parda', 'Indigena']
    means = pd.DataFrame(etnia, columns=['ETNIA'])

    # Iteração sobre as colunas dadas em 'columns'
    for column in columns:
        medias = []
        # Conversão da coluna para coluna númerica
        df.loc[:,column] = pd.to_numeric(df[column], errors='coerce')

        # Iteração sobre as etnias
        for i, etn in enumerate(etnia,1):
            # Calculando a média da coluna atual, considerando as linhas do 'campo' onde se verifica o código de etnia 'i'
            mean = df[column].loc[df[campo].str.strip() == str(i)].mean()
            # Registro da média na lista
            medias.append(mean)
        # Criação do DataFrame de média da coluna atual de todas as etnias
        column_mean = pd.DataFrame(medias, columns=[column + ' méd.'])
        # Concatenação da média da coluna no DataFrame final
        means = pd.concat([means, column_mean], axis=1)

    return(means)

def mean_uf(df, campo, columns):
    # Criação do DataFrame
    medias_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df['CODMUNNASC'].str.startswith(str(estados[estado]))
        df_filtered = df[filter]
        # Cálculo das médias
        media_uf = media(df_filtered, campo, columns)
        # Acionamento de coluna identificadora de estado
        media_uf['ESTADO'] = estado
        # Concatenação ao DataFrame final
        medias_uf = pd.concat([medias_uf, media_uf])
    return(medias_uf)        

def fr_acum(df, columns, n):

    dfr = pd.DataFrame()

    for column in columns:
        df.loc[:,column] = pd.to_numeric(df[column], errors='coerce')

        freq_count = df[column].value_counts()

        freq_total = freq_count.sum()

        data = pd.DataFrame([f'{column}'], columns=['CAMPO'])

        for fr in range(7,55,n):
            freq = (freq_count.loc[(freq_count.index < fr + n) & (freq_count.index > (fr))].sum())/(freq_total)
            col_name = [f'fr. idade {fr} - {fr + n}']
            tmp = pd.DataFrame([freq], columns=col_name)
            data = pd.concat([data, tmp], axis=1)

        dfr = pd.concat([dfr, data])
    return(dfr)

def fr_acum_uf(df, columns, n):
    # Criação do DataFrame
    fracum_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df['CODMUNNASC'].str.startswith(str(estados[estado]))
        df_filtered = df[filter]
        # Cálculo das freq. acumuladas
        fra_uf = fr_acum(df_filtered, columns, n)
        # Acionamento de coluna identificadora de estado
        fra_uf['ESTADO'] = estado
        # Concatenação ao DataFrame final
        fracum_uf = pd.concat([fracum_uf, fra_uf])
    return(fracum_uf)