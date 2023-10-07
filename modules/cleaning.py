import pandas as pd

def file_to_list(path: str) -> list[str]:
    """Função que recebe um arquivo .txt e retorna uma lista em que
    cada linha do arquivo é um elemento da lista.

    Parameters
    ----------
    path : str
        Endereço do arquivo.

    Returns
    -------
    list[str]
        Lista com as linhas do arquivo.
    """

    # Lista que conterá as linhas do arquivo
    txt_list = []
    
    try:
        with open(path, 'r') as fp:
            for line in fp:
                # Remove a quebra de linha da string
                element = line[:-1]

                # Adiciona linha do arquivo à lista
                txt_list.append(element)
    except FileNotFoundError:
        print("Arquivo não encontrado.")

    return txt_list


def filter_rows(df: pd.DataFrame, restrictions: dict) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base em um conjunto de restrições
    para cada campo a ser verificado. Retorna um DataFrame somente com as linhas
    que satisfazem todas as restrições.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado.
    restrictions : dict
        Dicionário em que cada chave é uma coluna do DataFrame e o valor é uma
        lista com os valores aceitos para aquela coluna.

    Returns
    -------
    pd.DataFrame
        DataFrame somente com as linhas que satisfazem as restrições.
    """

    for restriction in restrictions:
        # Nome da coluna e valores aceitos para a coluna
        column = restriction
        subset = restrictions[column]

        try:
            # Encontra as linhas válidas e filtra o DataFrame
            valid_rows = df[column].isin(subset)
            df = df[valid_rows]
        except KeyError:
            print("Coluna inválida.")
    
    return df


def filter_by_z_score(df: pd.DataFrame, columns: list[str], limit: float) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base no Z-Score de cada elemento. Retorna um
    DataFrame somente com as linhas em que o Z-Score de cada elemento é menor do que o
    limite, em módulo.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado.
    columns : list[str]
        Lista com as colunas a serem consideradas no filtro.
    limit : float
        Z-Score máximo para que um elemento seja considerado válido.

    Returns
    -------
    pd.DataFrame
       DataFrame somente com as linhas em que o z-score de cada elemento está
       abaixo do limite estabelecido.
    """

    # Média e desvio padrão das colunas
    mean = df.mean()
    std_dev = df.std()
  
    try:
        # DataFrame com o Z-Score de cada elemento em relação à coluna
        z_scores = (mean - df) / std_dev
    except ZeroDivisionError:
        return df
    
    for column in columns:
        try:
            # Filtra o DataFrame com as linhas cujo Z-Score é menor do que o limite
            valid_rows = abs(z_scores[column]) < limit
            df = df[valid_rows]
        except KeyError:
            print("Coluna inválida.")

    return df
