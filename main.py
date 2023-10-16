import pandas as pd
import numpy as np
import subprocess
import os

from modules import cleaning


def main():
    if not os.path.exists('data/dados.csv'):
        print('-' * 80)
        print('Limpando base de dados...')

        cleaning.load_data('data/SINASC_2021.csv', 'data/dados.csv')
    
    print('-' * 80)
    print('Gerando imagens para análise 1...')

    subprocess.run(['python', 'modules/analysis/yure/make_images.py'])

    print('-' * 80)
    print('Gerando imagens para análise 2...')

    subprocess.run(['python', 'modules/analysis/saulo/make_images.py'])

    print('-' * 80)
    print('Gerando imagens para análise 3...')

    subprocess.run(['python', 'modules/analysis/henzo/make_images.py'])

    print('-' * 80)
    print('Gerando imagens para análise 4...')

    subprocess.run(['python', 'modules/analysis/mattos/make_images.py'])


if __name__ == "__main__":
    main()