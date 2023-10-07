import pandas as pd
import numpy as np
from modules import cleaning

def main():
    cleaning.load_data('data/SINASC_2021.csv', 'data/saida.csv')
    df = pd.read_csv('data/saida.csv', encoding="unicode_escape", engine="python", sep=";")
    print(df.head())

if __name__ == "__main__":
    main()