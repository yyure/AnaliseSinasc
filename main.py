import pandas as pd
import modules 

def main():
    caminho_arquivo = 'SINASC_2021.csv'

    df = pd.read_csv(caminho_arquivo, encoding="unicode_escape", engine="python", sep=";", iterator=True, chunksize=1000)
    for chunk in df:
        print(chunk.head())

    colunas_para_remover = modules.files_to_list('columns_to_remove.txt')

    df.drop(columns=colunas_para_remover, inplace=True)

    print(df)

if __name__ == "__main__":
    main()
    