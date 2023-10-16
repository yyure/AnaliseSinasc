import pandas as pd
import numpy as np
import sys

import statistics


sys.path.append('../../..')

df = pd.read_csv('data/dados.csv', sep=';', engine='python')

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

# Colunas as quais se deve calcular as frequências
cols_to_fri = {
    'IDADEMAE' : 3,
    'ESCMAE'  : 1,
    'CONSPRENAT' : 2,
}

# Criação de dados estatísticos de cada município das colunas fornecidas
df0 = statistics.filter_uf(df, 'CODMUNNASC', ['IDADEMAE', 'ESCMAE', 'CONSPRENAT'])
for estado in df0:
    df0[estado].to_csv(f'modules/analysis/mattos/Data_UF/Data_{estado}.csv', mode='a', sep=';')

# Criando arquivos .csv das frequências relativas visando geração mais rápida de imagens
for column in cols_to_fri:
    name = column.lower()
    df1 = statistics.fr_relativa(df, column, cols_to_fri[column])
    df1.to_csv(f'modules/analysis/mattos/Freq_Relativa/FRI{name}_BR.csv', mode='a', sep=';')
for column in cols_to_fri:
    name = column.lower()
    df2 = statistics.frelat_ufs(df,'CODMUNNASC', column, cols_to_fri[column])
    df2.to_csv(f'modules/analysis/mattos/Freq_Relativa/FRI{name}_UF.csv', mode='a', sep=';')