import pandas as pd
import numpy as np
import doctest

def file_to_list(path: str) -> list[str]:
    """Função que recebe um arquivo .txt e retorna uma lista em que
    cada linha do arquivo é um elemento da lista. Caso o arquivo não seja
    encontrado será retornada uma lista vazia.

    Parameters
    ----------
    path : str
        Endereço do arquivo.

    Returns
    -------
    list[str]
        Lista com as linhas do arquivo.

    Examples
    --------
    Primeiro elemento da lista gerada pelo arquivo 'data/columns_to_remove.txt'
    >>> file_to_list('data/columns_to_remove.txt')[0]
    'CODMUNNASC'

    Retorna uma lista vazia e exibe uma mensagem de erro se o arquivo não existir
    >>> file_to_list('arquivo_nao_existente')
    Erro: Arquivo arquivo_nao_existente não encontrado.
    []
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
        print(f"Erro: Arquivo {path} não encontrado.")

    return txt_list


def filter_rows(df: pd.DataFrame, restrictions: dict[str,list]) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base em um conjunto de restrições
    para cada campo a ser verificado. Retorna um DataFrame somente com as linhas
    que satisfazem todas as restrições.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a ser filtrado.
    restrictions : dict[str,list]
        Dicionário em que cada chave é uma coluna do DataFrame e o valor é uma
        lista com os valores aceitos para aquela coluna.

    Returns
    -------
    pd.DataFrame
        DataFrame somente com as linhas que satisfazem as restrições.

    Examples
    --------
    
    """

    for restriction in restrictions:
        # Nome da coluna e valores aceitos para a coluna
        column = restriction
        subset = restrictions[column]

        try:
            # Encontra as linhas válidas e filtra o DataFrame
            valid_rows = df[column].isin(subset)
            df = df[valid_rows]
        except KeyError as error:
            print(f"Erro: Coluna {error} não encontrada.")
    
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
            valid_rows = df.loc[abs(z_scores[column]) < limit]
            df = valid_rows
        except KeyError as error:
            print(f"Erro: Coluna {error} não encontrada.")

    return df


def load_data(path_input: str, path_output: str):
    """Função que recebe o arquivo com o conjunto de dados brutos e gera
    um arquivo com os dados tratados.

    Parameters
    ----------
    path_input : str
        Endereço do arquivo com os dados brutos
    path_output : str
        Endereço em que será criado o arquivo com os dados tratados.
    """

    # Colunas a serem removidas do DataFrame
    columns_to_remove = file_to_list('data/columns_to_remove.txt')

    # Dicionário com as colunas categóricas e os valores aceitos
    restrictions = {'LOCNASC' : [1,2,3,4,5], 'ESTCIVMAE' : [1,2,3,4,5,9], 'ESCMAE' : [1,2,3,4,5,9],
                  'GESTACAO' : [1,2,3,4,5,6,9], 'GRAVIDEZ' : [1,2,3,9], 'PARTO' : [1,2,3,4,5,9],
                  'CONSULTAS' : [1,2,3,4,9], 'SEXO' : [1,2,0], 'RACACOR' : [1,2,3,4,5], 'RACACORMAE' : [1,2,3,4,5],
                  'CONSULTAS' : [1,2,3,4,9], 'STTRABPART' : [1,2,3,9], 'STCESPARTO' : [1,2,3,9], 'ESCMAE2010' : [0,1,2,3,4,5,9]}
    
    try:
        df = pd.read_csv(path_input, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=100000)
    except FileNotFoundError:
        print(f"Erro: Arquivo {path_input} não encontrado.")
        return

    for chunk in df:
        # Muda o índice do DataFrame para o número do registro
        chunk.set_index('CONTADOR', inplace=True)

        chunk.drop_duplicates(inplace=True)
        
        # Remove as colunas que não serão utilizadas
        chunk.drop(columns=columns_to_remove, inplace=True, errors="ignore")

        chunk.dropna(subset=["LOCNASC", "RACACOR", "SEXO", "RACACORMAE", "MESPRENAT"], inplace=True)

        # Preenche as linhas em que SEMAGESTAC é vazio, trocando pela média dos valores
        semagestac_mean = chunk['SEMAGESTAC'].mean()
        chunk['SEMAGESTAC'].fillna(semagestac_mean, inplace=True)

        # Preenche os valores das colunas com zero
        columns_to_fill = ['QTDFILVIVO', 'QTDFILMORT', 'QTDGESTANT', 'QTDPARTNOR', 'QTDPARTCES']
        chunk[columns_to_fill] = chunk[columns_to_fill].fillna(0)

        chunk.dropna(inplace=True)

        # Converte o tipo de dados do DataFrame
        chunk = chunk.astype(np.int32)

        # Remove as linhas em que as colunas categóricas estão com algum valor não aceito
        chunk = filter_rows(chunk, restrictions)

        # Remove as linhas que possuem possíveis outliers em algumas colunas
        columns_to_filter = ['IDADEMAE', 'CONSULTAS', 'QTDGESTANT', 'QTDPARTNOR', 'QTDPARTCES', 'SEMAGESTAC', 'CONSPRENAT', 'MESPRENAT']
        chunk = filter_by_z_score(chunk, columns_to_filter, 4)

        # Salva o DataFrame no arquivo de saída
        chunk.to_csv(path_output, mode='a', header=True, index=True, sep=';')

if __name__ == "__main__":
    doctest.testmod(verbose=True)