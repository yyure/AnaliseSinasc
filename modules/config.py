import yaml

data = {
    'df_index' : 'CONTADOR',
    'columns_to_remove' : [
        'CODMUNNASC',
        'CODOCUPMAE',
        'CODMUNRES',
        'DTNASC',
        'APGAR1',
        'APGAR5',
        'PESO',
        'CODANOMAL',
        'HORANASC',
        'IDANOMAL',
        'CODESTAB',
        'DTCADASTRO',
        'DTRECEBIM',
        'ORIGEM',
        'CODCART',
        'NUMREGCART',
        'DTREGCART',
        'CODPAISRES',
        'NUMEROLOTE',
        'VERSAOSIST',
        'DIFDATA',
        'DTRECORIG',
        'NATURALMAE',
        'CODMUNNATU',
        'DTNASCMAE',
        'IDADEPAI',
        'DTULTMENST',
        'TPMETESTIM',
        'TPAPRESENT',
        'TPROBSON',
        'STDNEPIDEM',
        'STDNNOVA',
        'CODMUNCART',
        'CODUFNATU',
        'TPNASCASSI',
        'DTRECORIGA',
        'TPFUNCRESP',
        'TPDOCRESP',
        'DTDECLARAC',
        'SERIESCMAE'
    ],
    'restrictions' : {
        'LOCNASC' : [1,2,3,4,5],
        'ESTCIVMAE' : [1,2,3,4,5,9],
        'ESCMAE' : [1,2,3,4,5,9],
        'GESTACAO' : [1,2,3,4,5,6,9],
        'GRAVIDEZ' : [1,2,3,9],
        'PARTO' : [1,2,3,4,5,9],
        'CONSULTAS' : [1,2,3,4,9],
        'SEXO' : [1,2,0],
        'RACACOR' : [1,2,3,4,5],
        'RACACORMAE' : [1,2,3,4,5],
        'CONSULTAS' : [1,2,3,4,9],
        'STTRABPART' : [1,2,3,9],
        'STCESPARTO' : [1,2,3,9],
        'ESCMAE2010' : [0,1,2,3,4,5,9]
    },
    'columns_to_dropna' : [
        "LOCNASC",
        "RACACOR",
        "SEXO",
        "RACACORMAE",
        "MESPRENAT"
    ],
    'columns_to_fill_mean' : [
        'SEMAGESTAC'
    ],
    'columns_to_fill_zero' : [
        'QTDFILVIVO',
        'QTDFILMORT',
        'QTDGESTANT',
        'QTDPARTNOR',
        'QTDPARTCES'
    ],
    'columns_to_filter_by_z_score' : [
        'IDADEMAE',
        'CONSULTAS',
        'QTDGESTANT',
        'QTDPARTNOR',
        'QTDPARTCES',
        'SEMAGESTAC',
        'CONSPRENAT',
        'MESPRENAT'
    ],
    'z_score_limit' : 4
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
