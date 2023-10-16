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

def fr_relativa_aux(df: pd.DataFrame, column: str, n: int, i: int, j: int) -> pd.DataFrame:
    """Calcula as frequências relativas da coluna ``column``
    do DataFrame ``df`` em intervalos de comprimento ``n``
    respeitando os extremos ``i`` e ``j``.

    Parameters
    ----------
    df : DataFrame
        DataFrame com a coluna a ser analisada.
    column : str
        Nome da coluna analisada.
    n : int
        Tamanho dos intervalos usados no cálculo.
    i : int
        Menor dos dados considerados.
    j : int
        Maior dos dados considerados.

    Returns
    -------
    pd.DataFrame
        DataFrame com a frequência relativa dos dados
        da ``column`` segundo intervalos de comprimento
        ``n``.

    Examples
    --------
    Teste 1: fri com ``n=1``

    >>> data = {'Dados': [1, 1, 1, 2, 3, 2, 1, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 1
    >>> i = 1
    >>> j = 5
    >>> fri = fr_relativa_aux(df, column, n, i, j)
    >>> fri
       Dados  freq. relativa
    0      1           0.500
    1      2           0.250
    2      3           0.125
    3      4           0.000
    4      5           0.125

    Teste 2: fri com ``n!=1``

    >>> data = {'Dados': [1, 1, 1, 2, 3, 2, 1, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> i = 1
    >>> j = 5
    >>> fri = fr_relativa_aux(df, column, n, i, j)
    >>> fri
       Dados  freq. relativa
    0  1 a 3           0.750
    1  3 a 5           0.125
    2  5 a 7           0.125
    3  7 a 9           0.000

    Teste 3: Valores ausentes

    >>> data = {'Dados': [1, np.nan, 1, 2, 3, 2, np.nan, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> i = 1
    >>> j = 5
    >>> fri = fr_relativa_aux(df, column, n, i, j)
    >>> fri
       Dados  freq. relativa
    0  1 a 3        0.666667
    1  3 a 5        0.166667
    2  5 a 7        0.166667
    3  7 a 9        0.000000

    Teste 4: DataFrame vazio

    >>> data = {'Dados': []}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> i = 1
    >>> j = 5
    >>> fri = fr_relativa_aux(df, column, n, i, j)
    >>> ValueError: DataFrame fornecido é vazio.
    """
    # Verificando o DataFrame
    if df.empty:
        raise ValueError('DataFrame fornecido é vazio.')
    # Inicialização de listas para coleta dos dados obtidos
    intervals = []
    dados = []
    # Eliminação de valores ausentes
    df = df.dropna()
    # Total de observações
    total = len(df[column])
    # Iteração sobre o intervalo
    cur = i
    while cur < j + n:
        # Contagem de ocorrência no intervalo atual
        intervalo = df.loc[(df[column] >= cur) & (df[column] < cur + n)]
        count_intervalo = len(intervalo)
        # Adicionando identificador de intervalo
        if n == 1:
            intervals.append(f'{cur}')
        else:
            intervals.append(f'{cur} a {cur + n}')
        # Adiconamento da frequência relativa
        dados.append(count_intervalo / total)
        
        cur += n
    # Criação do DataFrame
    fri = pd.DataFrame({f'{column}': intervals, 'freq. relativa': dados})

    return fri

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

    Examples
    --------
    Teste 1: fri com ``n=1``

    >>> data = {'Dados': [1, 1, 1, 2, 3, 2, 1, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 1
    >>> fri = fr_relativa_aux(df, column, n)
    >>> fri
       Dados  freq. relativa
    0      1           0.500
    1      2           0.250
    2      3           0.125
    3      4           0.000
    4      5           0.125

    Teste 2: fri com ``n!=1``

    >>> data = {'Dados': [1, 1, 1, 2, 3, 2, 1, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> fri = fr_relativa_aux(df, column, n)
    >>> fri
       Dados  freq. relativa
    0  1 a 3           0.750
    1  3 a 5           0.125
    2  5 a 7           0.125
    3  7 a 9           0.000

    Teste 3: Valores ausentes

    >>> data = {'Dados': [1, np.nan, 1, 2, 3, 2, np.nan, 5]}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> fri = fr_relativa_aux(df, column, n)
    >>> fri
       Dados  freq. relativa
    0  1 a 3        0.666667
    1  3 a 5        0.166667
    2  5 a 7        0.166667
    3  7 a 9        0.000000

    Teste 4: DataFrame vazio

    >>> data = {'Dados': []}
    >>> df = pd.DataFrame(data)
    >>> column = 'Dados'
    >>> n = 2
    >>> fri = fr_relativa_aux(df, column, n)
    >>> ValueError: DataFrame fornecido é vazio.
    """
    # Verificando o DataFrame
    if df.empty:
        raise ValueError('DataFrame fornecido é vazio.')
    # Determinando intervalos extremos
    i = 0
    j = 0
    try:
        i = int(df[column].min())
        j = int(df[column].max())
    except KeyError:
        print(f'Erro: Coluna {column} não encontrada.')
    data = fr_relativa_aux(df, column, n, i, j)
    return data

def frelat_ufs(df: pd.DataFrame, cod_uf: str, column: str, n: int) -> pd.DataFrame:
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

    Examples
    --------
    Teste 1: Valores válidos
    
    >>> data = {'Estados': [12, 27, 31, 31, 12], 'Dados':[10, 5, 2, 7, 5]}
    >>> df = pd.DataFrame(data)
    >>> cod_uf = 'Estados'
    >>> column = 'Dados'
    >>> n = 3
    >>> fri = statics.frelat_ufs(df, cod_uf, column, n)
    >>> fri
         Dados  AC fri.  AL fri.  MG fri.
    0    2 a 5      0.0      0.0      0.5
    1    5 a 8      0.5      1.0      0.5
    2   8 a 11      0.5      0.0      0.0
    3  11 a 14      0.0      0.0      0.0

    Teste 2: Valores ausentes
    
    >>> data = {'Estados': [12, np.nan, 31, 31, 12], 'Dados':[10, np.nan, 2, np.nan, 5]}
    >>> df = pd.DataFrame(data)
    >>> cod_uf = 'Estados'
    >>> column = 'Dados'
    >>> n = 3
    >>> fri = statics.frelat_ufs(df, cod_uf, column, n)
    >>> fri
         Dados  AC fri.  MG fri.
    0    2 a 5      0.0      1.0
    1    5 a 8      0.5      0.0
    2   8 a 11      0.5      0.0
    3  11 a 14      0.0      0.0

    Teste 3: DataFrame vazio
    
    >>> data = {'Estados': [], 'Dados':[]}
    >>> df = pd.DataFrame(data)
    >>> cod_uf = 'Estados'
    >>> column = 'Dados'
    >>> n = 3
    >>> fri = statics.frelat_ufs(df, cod_uf, column, n)
    >>> ValueError: DataFrame fornecido é vazio.
    """
    # Verificando o DataFrame
    if df.empty:
        raise ValueError('DataFrame fornecido é vazio.')

    # Existência da coluna cod_uf
    if not cod_uf in df.columns:
        raise KeyError(f'Erro: Coluna {cod_uf} não encontrada')

    # Determinando intervalos extremos
    i = 0
    j = 0
    try:
        i = int(df[column].min())
        j = int(df[column].max())
    except KeyError:
        print(f'Erro: Coluna {column} não encontrada.')

    # Criação do DataFrame
    fri_uf = pd.DataFrame()
    # Iteração sobre os Estados
    counter = 1
    for estado in estados:
        # Filtração da base de dados de acordo com o código do Estado atual
        filter = df[cod_uf].astype(str).str.startswith(str(estados[estado]))
        if filter.any():
            # DataFrame filtrado
            df_filtered = df[filter]
            # Cálculo da frequência acumulada
            fre_uf = fr_relativa_aux(df_filtered, column, n, i, j)
            # Acionamento de coluna identificadora de Estado
            fre_uf.rename(columns={'freq. relativa':f'{estado} fri.'}, inplace=True)
            # Concatenação ao DataFrame final
            if counter == 1:
                fri_uf = pd.concat([fri_uf, fre_uf], axis=1)
                counter = 0
            else:
                fri_uf = pd.concat([fri_uf, fre_uf[f'{estado} fri.']], axis=1)
    # Tratamento de possíveis ``na``s próximos aos extremos
    fri_uf.fillna(0)
    return(fri_uf)

def filter_uf(df: pd.DataFrame, cod_uf: str, dados: list[str]) -> dict[str, pd.DataFrame]:
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
    # Existência da coluna cod_uf
    if not cod_uf in df.columns:
        raise KeyError(f'Erro: Coluna {cod_uf} não encontrada')

    # Criação do dicionário
    dic_uf = {}
    # Iteração sobre os Estados
    try:
        for estado in estados:
            # Filtrando as linhas de acordo com o Estado
            filter = df[cod_uf].astype(str).str.startswith(str(estados[estado]))
            if filter.any():
                # DataFrame filtrado
                df_filtered = df[filter]
                # Selecionamento das estatísticas
                dic_uf[estado] = df_filtered[dados].describe()
    except KeyError:
        raise KeyError(f'Erro: Alguma coluna de {dados} não encontrada.')

    return dic_uf

if __name__ == "__main__":
    doctest.testmod(verbose=True)