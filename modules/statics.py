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
    >>> data = data = {'Column_1': [np.nan, 1, 2, 2, 3, 4], 'Column_2': [5, 10, 5, np.nan, np.nan, 1], 'Column_3': [np.nan, 2, 9, 2, 0, 1]}
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
    return(medias_uf)        

def fr_relativa(df, columns, n):
    """Calcula a frequência relativa das colunas do DataFrame ``df``
    fornecidas em ``columns`` de acordo com o tamanho ``n``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    columns : [str]
        Lista com as colunas que se deseja obter as frequências
        relativas.
    n : int
        Tamanho dos intevalos onde se calcula a frequência.

    Returns
    -------
    pd.DataFrame\\
        DataFrame com as frequências relativas calculadas
        em intervalos de tamanho ``n`` para cada coluna
        fornecida em ``columns``.

    Important
    --------
    A função ainda precisa ser aprimorada para permitir os
    testes. Esta versão só funciona para o caso ``columns=['IDADEMAE']``\\
    Uma nova versão desta função saíra em breve.\\
    """
    # Criação do DataFrame
    dfr = pd.DataFrame()
    # Iteração sobre as colunas dadas em 'columns'
    for column in columns:
        # Conversão da coluna atual para coluna númerica
        df.loc[:,column] = pd.to_numeric(df[column], errors='coerce')
        # Cálculo das frequências
        freq_count = df[column].value_counts()
        # Soma de todas as frequências
        freq_total = freq_count.sum()
        # Criação do DataFrame que armazena as frequências relativas calculadas
        data = pd.DataFrame([f'{column}'], columns=['CAMPO'])
        # Iteração sobre os extremos do intervalo de 'freq_count' sobre o intervalo 'n'
        for fr in range(7,55,n):
            # Cálculo da frequência dado o intervalo
            freq = freq_count.loc[(freq_count.index < fr + n) & (freq_count.index > (fr))].sum()
            # Cálculo da frequência relativa
            freq_r = freq /freq_total
            # Coluna de identificação do intervalo calculado
            col_name = [f'fr. idade {fr} - {fr + n}']
            # DataFrame temporário para agrupar as informções do loop e permitir
            # o adicionamento no DataFrame final
            tmp = pd.DataFrame([freq_r], columns=col_name)
            # Concatenização dos da frequência relativa ao DataFrame final
            data = pd.concat([data, tmp], axis=1)
        # Reúnião das frequências relativas de cada coluna
        dfr = pd.concat([dfr, data])
    return(dfr)

def frelat_uf(df, columns, n):
    """Calcula a frequência relativa das colunas do DataFrame ``df``
    fornecidas em ``columns`` de acordo com o tamanho ``n`` agrupando
    por estado.
    \\
    \\
    Atenção: o DataFrame ``df`` fornecido deve contar a coluna
    'CODMUNNASC'.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado.
    columns : [str]
        Lista com as colunas que se deseja obter as frequências
        relativas.
    n : int
        Tamanho dos intevalos onde se calcula a frequência.

    Returns
    -------
    pd.DataFrame\\
        DataFrame com as frequências relativas de cada estado
        calculadas em intervalos de tamanho ``n`` para cada coluna
        fornecida em ``columns``.

    Important
    --------
    Os testes serão adicionados brevemente após a nova versão de
    ``fr_relativa``\\
    """
    # Criação do DataFrame
    fracum_uf = pd.DataFrame()
    # Iteração sobre os estados
    for estado in estados:
        # Filtração da base de dados de acordo com o código do estado atual
        filter = df['CODMUNNASC'].str.startswith(str(estados[estado]))
        df_filtered = df[filter]
        # Cálculo das freq. acumuladas
        fra_uf = fr_relativa(df_filtered, columns, n)
        # Acionamento de coluna identificadora de estado
        fra_uf['ESTADO'] = estado
        # Concatenação ao DataFrame final
        fracum_uf = pd.concat([fracum_uf, fra_uf])
    return(fracum_uf)
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