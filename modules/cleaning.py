import pandas as pd

def file_to_list(path: str) -> list[str]:
    """Função que transforma as linhas de um arquivo .txt em uma lista

    Parameters
    ----------
    path : str
        Endereço do arquivo

    Returns
    -------
    list[str]
        Lista com as linhas do arquivo
    """

    txt_list = []
    
    try:
        with open(path, 'r') as fp:
            for line in fp:
                # Remove a quebra de linha da string
                element = line[:-1]
                
                txt_list.append(element)
    except FileNotFoundError:
        print("Arquivo não encontrado.")

    return txt_list