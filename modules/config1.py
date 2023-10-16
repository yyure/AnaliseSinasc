import yaml

data = {
    'df_index' : 'CONTADOR',
    
    'colums_to_remove' :
    [
        'QTDGESTANT',
        'QTDPARTNOR',
        'QTDPARTCES'
    ]

}

def generate_config_file(path: str):
    """Gera o arquivo de configuração para a limpeza dos dados

    Parameters
    ----------
    path : str
        Endereço em que o arquivo será gerado.
    """

    with open(path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
