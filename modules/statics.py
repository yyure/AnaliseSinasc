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

def media_etnia(df, campo, columns):
    """Filtra as linhas correspondentes a etnia do ``campo`` e,
    posteriormente, efetua a media das colunas fornecidas
    em ``columns``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado.
    campo : str
        Coluna que contenha informações sobre etnia. Com base
        nela que o DataFrame será filtrado.
        \\
        Portanto, o campo
        deve conter apenas os nºs 1, 2, 3, 4, 5 que correspondem
        a cada uma das etnias.
    columns : [str]
        Lista com as colunas que se deseja obter a média

    Returns
    -------
    pd.DataFrame\\
        DataFrame com a média correspondente a cada etnia.

    Examples
    --------
    # Teste 1: Média das colunas com base na etnia
    >>> data = {'Column_1': [1, 1, 2, 2, 3, 4], 'Column_2': [5, 10, 5, 7, 1, 1], 'Column_3': [5, 2, 9, 2, 0, 1]}
    >>> df = pd.DataFrame(data)
    >>> columns = ['Column_2', 'Column_3']
    >>> means = media(df, 'Column_1', columns)
    >>> means
          ETNIA  Column_2 méd.  Column_3 méd.
    0    Branca            7.5            3.5
    1     Preta            6.0            5.5
    2   Amarela            1.0            0.0
    3     parda            1.0            1.0
    4  Indigena            NaN            NaN

    # Teste 2: Valores ausentes
    >>> data = {'Column_1': [np.nan, 1, 2, 2, 3, 4], 'Column_2': [5, 10, 5, np.nan, np.nan, 1], 'Column_3': [np.nan, 2, 9, 2, 0, 1]}
    >>> df = pd.DataFrame(data)
    >>> columns = ['Column_2', 'Column_3']
    >>> means = media(df, 'Column_1', columns)
    >>> means
          ETNIA  Column_2 méd.  Column_3 méd.
    0    Branca           10.0            2.0
    1     Preta            5.0            5.5
    2   Amarela            NaN            0.0
    3     parda            1.0            1.0
    4  Indigena            NaN            NaN

    # Teste 3: DataFrame vazio
    >>> df = pd.DataFrame(columns=['Column_1', 'Column_2', 'Column_3'])
    >>> columns = ['Column_2', 'Column_3']
    >>> means = media(df, 'Column_1', columns)
    >>> means
          ETNIA  Column_2 méd.  Column_3 méd.
    0    Branca            NaN            NaN
    1     Preta            NaN            NaN
    2   Amarela            NaN            NaN
    3     parda            NaN            NaN
    4  Indigena            NaN            NaN
    """
    # Conversão da campo para coluna númerica
    df.loc[:,campo] = pd.to_numeric(df[campo], errors='coerce')

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
            mean = df[column].loc[df[campo] == i].mean()
            # Registro da média na lista
            medias.append(mean)
        # Criação do DataFrame de média da coluna atual de todas as etnias
        column_mean = pd.DataFrame(medias, columns=[column + ' méd.'])
        # Concatenação da média da coluna no DataFrame final
        means = pd.concat([means, column_mean], axis=1)

    return(means)

def mediauf_etnia(df, campo, columns):
    """Filtra as linhas correspondentes a etnia do ``campo`` e,
    posteriormente, efetua a media das colunas fornecidas
    em ``columns`` agrupando por Estado.
    \\
    \\
    Atenção: o DataFrame ``df`` fornecido deve contar a coluna
    'CODMUNNASC'.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado.
    campo : str
        Coluna que contenha informações sobre etnia. Com base
        nela que o DataFrame será filtrado.
        \\
        Portanto, o campo
        deve conter apenas os nºs 1, 2, 3, 4, 5 que correspondem
        a cada uma das etnias.
    columns : [str]
        Lista com as colunas que se deseja obter a média

    Returns
    -------
    pd.DataFrame\\
        DataFrame com as médias estaduais correspondente a cada
        etnia.

    Examples
    --------
    # Teste 1: Média das colunas com base na etnia
    >>> data = {'Column_1': [1, 1, 2, 2, 3, 4], 'CODMUNNASC': [12, 27, 27, 16, 16, 16], 'Column_3': [5, 2, 9, 2, 0, 1]}
    >>> df = pd.DataFrame(data)
    >>> columns = ['Column_3']
    >>> means_uf = mediauf_etnia(df, 'Column_1', columns)
    >>> means_uf.head(15)
          ETNIA  Column_3 méd. ESTADO
    0    Branca            5.0     AC
    1     Preta            NaN     AC
    2   Amarela            NaN     AC
    3     parda            NaN     AC
    4  Indigena            NaN     AC
    0    Branca            2.0     AL
    1     Preta            9.0     AL
    2   Amarela            NaN     AL
    3     parda            NaN     AL
    4  Indigena            NaN     AL
    0    Branca            NaN     AP
    1     Preta            2.0     AP
    2   Amarela            0.0     AP
    3     parda            1.0     AP
    4  Indigena            NaN     AP

    # Teste 2: Valores ausentes
    >>> data = {'Column_1': [np.nan, np.nan, 2, 2, 3, 4], 'CODMUNNASC': [12, 27, np.nan, 16, 16, 16], 'Column_3': [5, np.nan, 9, 2, 0, 1]}
    >>> df = pd.DataFrame(data)
    >>> columns = ['Column_3']
    >>> means_uf = mediauf_etnia(df, 'Column_1', columns)
    >>> means_uf.head(15)
          ETNIA  Column_3 méd. ESTADO
    0    Branca            NaN     AC
    1     Preta            NaN     AC
    2   Amarela            NaN     AC
    3     parda            NaN     AC
    4  Indigena            NaN     AC
    0    Branca            NaN     AL
    1     Preta            NaN     AL
    2   Amarela            NaN     AL
    3     parda            NaN     AL
    4  Indigena            NaN     AL
    0    Branca            NaN     AP
    1     Preta            2.0     AP
    2   Amarela            0.0     AP
    3     parda            1.0     AP
    4  Indigena            NaN     AP

    # Teste 3: DataFrame vazio
    >>> df = pd.DataFrame(columns=['Column_1', 'CODMUNNASC', 'Column_3'])
    >>> columns = ['Column_3']
    >>> means_uf = mediauf_etnia(df, 'Column_1', columns)
    >>> means_uf.head()
          ETNIA  Column_3 méd. ESTADO
    0    Branca            NaN     AC
    1     Preta            NaN     AC
    2   Amarela            NaN     AC
    3     parda            NaN     AC
    4  Indigena            NaN     AC
    """
    # Conversão de 'CODMUNNASC' para tipo string
    df['CODMUNNASC'] = df['CODMUNNASC'].astype(str)

    # Criação do DataFrame
    medias_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df['CODMUNNASC'].str.startswith(str(estados[estado]))
        df_filtered = df[filter]
        # Cálculo das médias
        media_uf = media_etnia(df_filtered, campo, columns)
        # Acionamento de coluna identificadora de estado
        media_uf['ESTADO'] = estado
        # Concatenação ao DataFrame final
        medias_uf = pd.concat([medias_uf, media_uf])
    medias_uf.set_index('ESTADO', inplace=True)
    return(medias_uf)        

def fr_relativa_aux(column, n, i, j, value_counts):
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
            intervals.append(f'{k + 1}')
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

def fr_relativa(df, column, n):
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
    # Cópia do DataFrame, visando evitar possíveis alterações no original
    df_cpy = df
    # Conversão da coluna de análise para coluna númerica
    df_cpy.loc[:,column] = pd.to_numeric(df_cpy[column], errors='coerce')
    # Extração da coluna
    col = df_cpy[column]
    # Contagem de ocorrências
    value_counts = col.value_counts()
    # Determinando intervalos extremos
    i = int(value_counts.index.min())
    j = int(value_counts.index.max())
    # Cálculo da frequência relativa
    data = fr_relativa_aux(column, n, i, j, value_counts)
    return data

def frelat_ufs(df, cod_uf, column, n):
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

    # Cópia do DataFrame, visando evitar possíveis alterações no original
    df_cpy = df
    # Conversão da coluna de análise para coluna númerica
    df_cpy.loc[:,column] = pd.to_numeric(df_cpy[column], errors='coerce')
    # Extração da coluna
    col = df_cpy[column]
    # Contagem de ocorrências
    counts = col.value_counts()
    # Determinando intervalos extremos
    i = int(counts.index.min())
    j = int(counts.index.max())
    # Criação do DataFrame
    fri_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Cálculo das freq. acumuladas
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df_cpy[cod_uf].str.startswith(str(estados[estado]))
        df_filtered = df_cpy[filter]
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
    # Prechimento de cedulas vazias, que podem aparecer próximos aos extremos i e j
    fri_uf.fillna(0)
    return(fri_uf)
    