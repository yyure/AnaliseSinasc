import unittest
import pandas as pd
import pandas.testing as pd_testing
import numpy as np
import io
import sys
import os

import cleaning

class TestCleaning(unittest.TestCase):
    def assertDataFrameEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e
    

    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataFrameEqual)


    # Teste 1: função filter_rows com parâmetros válidos deve funcionar como esperado.
    def test_filter_rows_with_valid_restrictions(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        }
        df = pd.DataFrame(data)
        restrictions = {
            'A': [1, 2],
            'B': [4, 5]
        }

        result = cleaning.filter_rows(df, restrictions)
        expected = pd.DataFrame({'A': [1, 2], 'B': [4, 5]})

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(result, expected)
    
    # Teste 2: função filter_rows com restrições que não existem no DataFrame deve levantar erro
    def test_filter_rows_with_invalid_restrictions(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        }
        df = pd.DataFrame(data)
        restrictions = {
            'C': [1, 2]
        }

        # Verifica se afunção levanta o erro esperado
        with self.assertRaises(KeyError):
            cleaning.filter_rows(df, restrictions)
    
    
    # Teste 3: função filter_by_z_score com parâmetros válidos deve funcionar como esperado.
    def test_filter_by_z_score_valid_input(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3],
            'B': [4, 5, 1000]
        }
        df = pd.DataFrame(data)
        columns = ['B']
        limit = 1.0

        result = cleaning.filter_by_z_score(df, columns, limit)
        expected = pd.DataFrame({'A': [1, 2], 'B': [4, 5]})

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(result, expected)
    

    # Teste 4: função filter_by_z_score quando o DataFrame não é numérico deve levantar erro
    def test_filter_by_z_score_invalid_input_non_numeric(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': ['1', '2', '3']
        }
        df = pd.DataFrame(data)
        columns = ['A']
        limit = 1.0

        # Verifica se a função levanta o erro esperado
        with self.assertRaises(TypeError):
            cleaning.filter_by_z_score(df, columns, limit)
        
    
    # Teste 5: função filter_by_z_score quando o desvio padrão é zero não deve alterar a linha.
    def test_filter_by_z_score_zero_std_dev(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [0, 0, 0]
        }
        df = pd.DataFrame(data)
        columns = ['A']
        limit = 1.0

        result = cleaning.filter_by_z_score(df, columns, limit)
        expected = pd.DataFrame({'A': [0, 0, 0]})

        # Verifica se o DataFrame retornado pela função é o esperado.
        self.assertEqual(result, expected)
    
    # Teste 6: função filter_by_z_score quando a coluna não existe deve levantar erro.
    def test_filter_by_z_score_invalid_input_columns(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        columns = ['B']
        limit = 1.0

        # Verifica se a função levanta o erro esperado
        with self.assertRaises(KeyError):
            cleaning.filter_by_z_score(df, columns, limit)

    
    # Teste 7: função fill_columns com parâmetros válidos deve funcionar como esperado.
    def test_fill_columns_valid_input(self):
        # Parâmetros que serão passados para a função
        data = {
            'A': [1, 2, np.NaN],
            'B': [np.NaN, np.NaN, np.NaN]
        }
        df = pd.DataFrame(data)
        columns_values = {
            'A': 3,
            'B': 0
        }

        result = cleaning.fill_columns(df, columns_values)

        # Quantidade de np.NaN no DataFrame
        nan_count = result['A'].isna().sum() + result['B'].isna().sum()

        self.assertEqual(nan_count, 0)
    
    # Teste 8: função fill_columns quando uma coluna no dicionário não existe no DataFrame deve levantar erro
    def test_fill_columns_invalid_input_columns(self):
        # Parâmetros que serão passados para a função
        data = {
            'A': [1, 2, np.NaN],
            'B': [np.NaN, np.NaN, np.NaN]
        }
        df = pd.DataFrame(data)
        columns_values = {
            'A': 3,
            'C': 0
        }

        # Verifica se a função levanta o erro esperado
        with self.assertRaises(KeyError):
            cleaning.fill_columns(df, columns_values)

    
    # Teste 9: função load_data quando o arquivo com os dados de entrada não existe deve levantar erro
    def test_load_data_input_file_not_exists(self):
        # Parâmetros que serão passados para a função.
        path_input = 'input.csv'
        path_output = 'output.csv'
        
        # Verifica se a função levanta o erro esperado
        with self.assertRaises(FileNotFoundError):
            cleaning.load_data(path_input, path_output)

    
    # Teste 10: função load_data com entrada inválida não deve criar o arquivo com os dados de saída.
    def test_load_data_invalid_input_create_output_file(self):
        # Parâmetros que serão passados para a função
        path_input = 'input.csv'
        path_output = 'output.csv'

        # Cria o arquivo de entrada 
        data = {
            'A': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        df.to_csv(path_input, index=False)

        # Verifica se a função levanta o erro esperado
        with self.assertRaises(KeyError):
            cleaning.load_data(path_input, path_output)

        # Verifica se o arquivo de saída existe
        self.assertTrue(not os.path.exists(path_output))

        # Remove os arquivos criados
        os.remove(path_input)


if __name__ == "__main__":
    unittest.main(buffer=True)