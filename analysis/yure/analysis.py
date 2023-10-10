import pandas as pd
import numpy as np

def dados_racacormae_consprenat(path: str) -> pd.DataFrame:
    """Função que recebe um arquivo csv e transforma os dados nesse arquivo em um
    DataFrame cujo índice é a coluna 'RACACORMAE' e as colunas são 'NUMCONSULTAS'
    e 'NUMREGISTROS', onde 'NUMCONSULTAS' é o número de consultas de pré-natal
    realizadas por pessoas de determinada raça/cor e 'NUMREGISTROS' é a quantidade
    de pessoas de determinada raça/cor.

    Parameters
    ----------
    path : str
        Endereço do arquivo.

    Returns
    -------
    pd.DataFrame
        DataFrame gerado.
    """
    # Cria o índice que será usado no DataFrame
    racacormae_values = [1, 2, 3, 4, 5]
    index = pd.Index(racacormae_values, name='RACACORMAE')

    df = pd.read_csv(path, encoding="unicode_escape", engine="python", sep=";", chunksize=100000)

    data_df = pd.DataFrame(data=None, index=index, columns=['NUMCONSULTAS', 'NUMREGISTROS'])
    data_df.fillna(0, inplace=True)

    for chunk in df:
        # Seleciona as colunas que serão utilizadas
        try: 
            chunk = chunk[['RACACORMAE', 'CONSPRENAT']]
        except KeyError:
            print('Erro: o DataFrame não possui as colunas \'RACACORMAE\' e \'CONSPRENAT\'.')
            return data_df

        for racacor in racacormae_values:
            raca_chunk = chunk.loc[chunk['RACACORMAE'] == racacor]

            # Adiciona o número de consultas e de registros no DataFrame data_df
            data_df.loc[racacor, 'NUMCONSULTAS'] += raca_chunk['CONSPRENAT'].sum()
            data_df.loc[racacor, 'NUMREGISTROS'] += len(raca_chunk)
    
    return data_df


def dados_racacormae_locnasc(path: str) -> pd.DataFrame:
    """Função que recebe um arquivo csv e transforma os dados nesse arquivo em um
    DataFrame cujos índices são 'RACACORMAE' e 'LOCNASC', e possui a coluna 'NUMREGISTROS',
    com a quantidade de registros de nascimento com mães de determinada raça/cor em um
    determinado tipo de local. 

    Parameters
    ----------
    path : str
        Endereço do arquivo.

    Returns
    -------
    pd.DataFrame
        DataFrame gerado.
    """
    # Cria o índice que será usado no DataFrame
    racacormae_values = [1, 2, 3, 4, 5]
    locnasc_values = [1, 2, 3, 4, 5]
    index_tuples = [(racacormae, locnasc) for racacormae in racacormae_values for locnasc in locnasc_values]
    multi_index = pd.MultiIndex.from_tuples(index_tuples, names=['RACACORMAE', 'LOCNASC'])

    df = pd.read_csv(path, encoding="unicode_escape", engine="python", sep=";", chunksize=100000)

    data_df = pd.DataFrame(data=None, index=multi_index, columns=['NUMREGISTROS'])
    data_df.fillna(0, inplace=True)

    for chunk in df:
        for racacor in racacormae_values:
            for locnasc in locnasc_values:
                # Encontra a quantidade de registros com base em 'RACACORMAE' e 'LOCNASC' e adiciona no DataFrame final
                try:
                    count = len(chunk.loc[(chunk['RACACORMAE'] == racacor) & (chunk['LOCNASC'] == locnasc)])
                except KeyError:
                    print('Erro: o DataFrame não possui as colunas \'RACACORMAE\' e \'LOCNASC\'.')
                    return data_df
                
                data_df.loc[racacor, locnasc] += count

    return data_df


def dados_racacormae_parto(path: str) -> pd.DataFrame:
    """Função que recebe um arquivo csv e transforma os dados nesse arquivo em um
    DataFrame cujo índice é 'RACACORMAE' e as colunas são 'QTDPARTNOR' e 'QTDPARTCES',
    onde 'QTDPARTNOR' é a quantidade total de partos normais e 'QTDPARTCES' é a
    quantidade total de partos cesários.

    Parameters
    ----------
    path : str
        Endereço do arquivo

    Returns
    -------
    pd.DataFrame
        DataFrame gerado.
    """
    # Cria o índice que será usado no DataFrame
    racacormae_values = [1, 2, 3, 4, 5]
    index = pd.Index(racacormae_values, name='RACACORMAE')

    df = pd.read_csv(path, encoding="unicode_escape", engine="python", sep=";", chunksize=100000)

    data_df = pd.DataFrame(data=None, index=index, columns=['QTDPARTNOR', 'QTDPARTCES'])
    data_df.fillna(0, inplace=True)

    for chunk in df:
        for racacor in racacormae_values:
            # Encontra a quantidade total de cada tipo de parto por raça
            try:
                raca_chunk = chunk.loc[chunk['RACACORMAE'] == racacor]
                count_partnor = len(raca_chunk.loc[raca_chunk['PARTO'] == 1])
                count_partces = len(raca_chunk.loc[raca_chunk['PARTO'] == 2])
            except KeyError:
                print('Erro: o DataFrame não possui as colunas \'RACACORMAE\' e \'PARTO\'.')
                return data_df

            data_df.loc[racacor, 'QTDPARTNOR'] += count_partnor
            data_df.loc[racacor, 'QTDPARTCES'] += count_partces
    
    return data_df
