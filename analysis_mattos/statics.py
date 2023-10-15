import pandas as pd
import numpy as np
import doctest

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

def fr_relativa_aux(column: str, n: int, i: int, j: int, value_counts: pd.Series) -> pd.DataFrame:
    """Calcula as frequências relativas a partir das frequências
    dos dados observados em ``value_counts`` em intervalos de
    comprimento ``n`` respeitando os extremos ``i`` e ``j``.

    Parameters
    ----------
    column : str
        Nome da coluna analisada.
    n : int
        Tamanho dos intervalos usados no cálculo.
    i : int
        Menor dos dados considerados.
    j : int
        Maior dos dados considerados.
    value_counts : DataFrame
        DataFrame com as frequências de ocorrência dos
        dados observados.

    Returns
    -------
    pd.DataFrame
        DataFrame com a frequência relativa dos dados
        observados segundo intervalos de comprimento
        ``n``.
    """
    # Número total de observações ou contagens
    total_counts = value_counts.sum()
    # Inicialização de listas para coleta dos dados obtidos
    intervals = []
    dados = []
    # Iteração item por item
    if n == 1:
        for k in range(i,j):
            # Obtenção da frequência em que 'k' surge na coluna fornecida
            fr = value_counts.loc[value_counts.index == k + 1].sum()
            # Cálculo da frequência relativa
            frel = fr / total_counts
            # Adicionamento das informações obtidas às listas
            dados.append(frel)
            intervals.append(f'{k}')
        # Criação do DataFrame com as frequências relativas
        data = pd.DataFrame({f'{column}': intervals, 'freq. relativa': dados})
    # Iteração por intervalo
    else:
        for k in range(i,j,n):
            # Obtenção da frequência em que 'k' surge dentro do intervalo [k, k+n) na coluna fornecida
            fr = value_counts.loc[(value_counts.index < k + n) & (value_counts.index >= k)].sum()
            #Cálculo da frequência relativa
            frel = fr / total_counts
            # Adicionamento das informações obtidas às listas
            dados.append(frel)
            intervals.append(f'{k} a {k + n}')
        # Criação do DataFrame com as frequências relativas
        data = pd.DataFrame({f'{column}': intervals, 'freq. relativa': dados})
    return data

def fr_relativa(df: pd.DataFrame, column: str, n: int) -> pd.DataFrame:
    """
    Calcula as frequências relativas dos dados observados em
    uma coluna do DataFrame ``df`` em intervalos de
    comprimento ``n``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com os dados para o cálculo.
    column : str
        Coluna de ``df`` que se deseja obter as frequências
        relativas
    n : int
        Tamanho dos intervalos usados no cálculo.        

    Returns
    -------
    pd.DataFrame
        DataFrame com as frequências relativas dos dados
        observados segundo intervalos de comprimento
        ``n``.
    """
    # Extração da coluna
    col = df[column]
    # Contagem de ocorrências
    value_counts = col.value_counts()
    # Determinando intervalos extremos
    i = int(value_counts.index.min())
    j = int(value_counts.index.max())
    data = fr_relativa_aux(column, n, i, j, value_counts)
    return data

def frelat_ufs(df: po.DataFrame, cod_uf: str, column: str, n: int) -> pd.DataFrame:
    """Calcula as frequências relativas (para cada Estado) de uma
    coluna do DataFrame ``df`` fornecido em intervalos de
    comprimento ``n``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    cod_uf : str
        Coluna de ``df`` na qual se encontram os códigos dos
        municípios ou Estados brasileiros segundo o IBGE.
    column : str
        Coluna de ``df`` que se deseja obter as frequências
        relativas
    n : int
        Tamanho dos intevalos onde se calcula a frequência.

    Returns
    -------
    pd.DataFrame
        DataFrame com as frequências relativas de cada Estado
        dos dados observados segundo intervalos de comprimento
        ``n``.
    """
    # Extração da coluna
    col = df[column]
    # Contagem de ocorrências
    counts = col.value_counts()
    # Determinando intervalos extremos
    i = int(counts.index.min())
    j = int(counts.index.max())
    # Criação do DataFrame
    fri_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df[cod_uf].astype(str).str.startswith(str(estados[estado]))
        df_filtered = df[filter]
        # Extração da coluna
        col_filtered = df_filtered[column]
        # Contagem de ocorrências
        value_counts = col_filtered.value_counts()
        # Cálculo da frequência acumulada
        fre_uf = fr_relativa_aux(column, n, i, j, value_counts)
        # Acionamento de coluna identificadora de estado
        fre_uf.rename(columns={'freq. relativa':f'{estado} fri.'}, inplace=True)
        # Concatenação ao DataFrame final
        if estado == 'AC':
            fri_uf = pd.concat([fri_uf, fre_uf], axis=1)    
        else:
            fri_uf = pd.concat([fri_uf, fre_uf[f'{estado} fri.']], axis=1)
    #fracum_uf.set_index('ESTADO', inplace=True)
    fri_uf.fillna(0)
    return(fri_uf)

def filter_uf(df: pd.DataFrame, cod_uf: str, columns: list[str]) -> dict[str, pd.DataFrame]:
    """Cria um dicionário onde cada chave corresponde a um Estado
    e o valor de cada chave é um DataFrame com as estatísticas do
    Estado referentes as colunas solicitadas em ``columns``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    cod_uf : str
        Coluna de ``df`` na qual se encontram os códigos dos
        municípios ou Estados brasileiros segundo o IBGE.
    columns : list[str]
        Lista das colunas que se devem obter as estatísticas
        no DataFrame final.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dicionário onde cada chave corresponde a um Estado (e.g. MG)
        e o valor de cada chave é o DataFrame daquele Estado com as
        estatísticas referentes as colunas solicitadas em ``columns``.
    """
    # Criação do dicionário
    dic_uf = {}
    # Iteração sobre os Estados
    for estado in estados:
        # Filtrando as linhas de acordo com o Estado
        filter = df[cod_uf].astype(str).str.startswith(str(estados[estado]))
        # DataFrame filtrado
        df_filtered = df[filter]
        # Selecionamento das estatísticas
        dic_uf[estado] = df_filtered[columns].describe()
    return dic_uf

if __name__ == "__main__":
    doctest.testmod(verbose=True)