import unittest
import pandas as pd
import pandas.testing as pd_testing
import numpy as np
import os

import analysis


class TestAnalysis(unittest.TestCase):
    def assertDataFrameEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e
    
    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataFrameEqual)

    # Teste 1: Função recebe arquivo de entrada com as colunas necessárias
    def test_dados_racacormae_consprenat_valid_input(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'CONSPRENAT': [8, 7, 9, 6, 8]
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_consprenat('input.csv')

        # Retorno esperado da função
        expected = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'NUMCONSULTAS': [8, 7, 9, 6, 8],
            'NUMREGISTROS': [1, 1, 1, 1, 1],
            'MEDIA': [8.0, 7.0, 9.0, 6.0, 8.0]
        })
        expected.set_index('RACACORMAE', inplace=True)

        self.assertEqual(result, expected)

        os.remove('input.csv')

    # Teste 2: Se o arquivo de entrada não existir, deve levantar o erro FileNotFoundError
    def test_dados_racacormae_consprenat_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            analysis.dados_racacormae_consprenat('')
    
    # Teste 3: Se a coluna 'CONSPRENAT' não existir, a função deve retornar um DataFrame apenas com zeros
    def test_dados_racacormae_consprenat_columns_not_exists(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_consprenat('input.csv')

        # Retorno esperado da função
        expected = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'NUMCONSULTAS': [0, 0, 0, 0, 0],
            'NUMREGISTROS': [0, 0, 0, 0, 0],
        })
        expected.set_index('RACACORMAE', inplace=True)

        self.assertEqual(result, expected)

        os.remove('input.csv')
    
    # Teste 4: # Função recebe arquivo de entrada com as colunas necessárias
    def test_dados_racacormae_locnasc_valid_input(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'LOCNASC': [3, 4, 1, 5, 2]
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_locnasc('input.csv')

        self.assertEqual(result.loc[1, 1]['NUMREGISTROS'], 0)

        os.remove('input.csv')
    
    # Teste 5: Se o arquivo de entrada não existir, deve levantar o erro FileNotFoundError
    def test_dados_racacormae_locnasc_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            analysis.dados_racacormae_locnasc('')
    
    # Teste 6: Se a coluna 'LOCNASC' não existir, a função deve retornar um DataFrame apenas com zeros
    def test_dados_racacormae_locnasc_column_not_exists(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_locnasc('input.csv')

        self.assertEqual(result.loc[1, 1]['NUMREGISTROS'], 0)

        os.remove('input.csv')
    
    # Teste 7: Função recebe arquivo de entrada com as colunas necessárias
    def test_dados_racacormae_parto_valid_input(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'LOCNASC': [1, 1, 1, 1, 1],
            'PARTO': [1, 2, 1, 2, 1]
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_parto('input.csv')

        # Retorno esperado da função
        expected = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'QTDPARTNOR': [1, 0, 1, 0, 1],
            'QTDPARTCES': [0, 1, 0, 1, 0]
        })
        expected.set_index('RACACORMAE', inplace=True)

        self.assertEqual(result, expected)

        os.remove('input.csv')
    
    # Teste 8: Se o arquivo de entrada não existir, deve levantar o erro FileNotFoundError
    def test_dados_racacormae_parto_file_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            analysis.dados_racacormae_locnasc('')
    
    # Teste 9: Se a coluna 'PARTO' não existir, a função deve retornar um DataFrame apenas com zeros
    def test_dados_racacormae_parto_columns_not_exists(self):
        # Cria o arquivo com o DataFrame
        data = pd.DataFrame({
            'RACACORMAE': [1, 2, 3, 4, 5],
            'LOCNASC': [1, 1, 1, 1, 1]
        })
        data.to_csv('input.csv', sep=';', header=True)

        result = analysis.dados_racacormae_parto('input.csv')

        self.assertEqual(result.loc[1]['QTDPARTNOR'], 0)

        os.remove('input.csv')


if __name__ == '__main__':
    unittest.main(buffer=True)