import unittest
import pandas as pd
import cleaning
import io
import sys
import os

class TestCleaning(unittest.TestCase):
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

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(result.shape, (2,2))
    
    # Teste 2: função filter_rows com restrições que não existem no DataFrame deve exibir mensagem de erro.
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

        # Mensagem de erro esperada.
        expected_error = 'Erro: Coluna C não encontrada.\n'

        # Lê o que é exibido no console quando a função é chamada.
        output = io.StringIO()
        sys.stdout = output
        cleaning.filter_rows(df, restrictions)
        sys.stdout = sys.__stdout__

        # Verifica se a mensagem de erro esperada aparece no console.
        self.assertEqual(expected_error, output.getvalue())
    
    # Teste 3: função filter_rows com restrições que não existem no DataFrame deve retornar o DataFrame original.
    def test_filter_rows_with_invalid_restrictions_return(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        }
        df = pd.DataFrame(data)
        restrictions = {
            'C': [1, 2]
        }

        result = cleaning.filter_rows(df, restrictions, verbose=False)

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(len(result), len(df))
    
    # Teste 4: função filter_by_z_score com parâmetros válidos deve funcionar como esperado.
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

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(result.shape, (2, 2))
    
    # Teste 5: função filter_by_z_score quando o DataFrame não é numérico deve exibr mensagem de erro.
    def test_filter_by_z_score_invalid_input_non_numeric(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': ['1', '2', '3']
        }
        df = pd.DataFrame(data)
        columns = ['A']
        limit = 1.0

        # Mensagem de erro esperada.
        expected_error = 'Erro: todos os valores devem ser numéricos.\n'

        # Lê o que é exibido no console quando a função é chamada.
        output = io.StringIO()
        sys.stdout = output
        cleaning.filter_by_z_score(df, columns, limit)
        sys.stdout = sys.__stdout__

        # Verifica se a mensagem de erro esperada aparece no console.
        self.assertEqual(expected_error, output.getvalue())
    
    # Teste 6: função filter_by_z_score quando o desvio padrão é zero não deve alterar a linha.
    def test_filter_by_z_score_zero_std_dev(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [0, 0, 0]
        }
        df = pd.DataFrame(data)
        columns = ['A']
        limit = 1.0

        result = cleaning.filter_by_z_score(df, columns, limit)

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(len(result), len(df))
    
    # Teste 7: função filter_by_z_score quando a coluna não existe deve retornar o DataFrame original.
    def test_filter_by_z_score_invalid_input_columns_return(self):
        # Parâmetros que serão passados para a função.
        data = {
            'A': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        columns = ['B']
        limit = 1.0

        result = cleaning.filter_by_z_score(df, columns, limit, verbose=False)

        # Verifica se o DataFrame retornado pela função tem o formato esperado.
        self.assertEqual(len(result), len(df))
    
    # Teste 8: função load_data quando o arquivo com os dados de entrada não existe deve exibir mensagem de erro.
    def test_load_data_input_file_not_exists(self):
        # Parâmetros que serão passados para a função.
        path_input = 'input.csv'
        path_output = 'output.csv'
        
        # Mensagem de erro esperada.
        expected_error = 'Erro: Arquivo input.csv não encontrado.\n'

        # Lê o que é exibido no console quando a função é chamada.
        output = io.StringIO()
        sys.stdout = output
        cleaning.load_data(path_input, path_output)
        sys.stdout = sys.__stdout__

        # Verifica se a mensagem de erro esperada aparece no console.
        self.assertEqual(expected_error, output.getvalue())
    
    # Teste 9: função load_data deve criar o arquivo com os dados de saída.
    def test_load_data_create_output_file(self):
        # Parâmetros que serão passados para a função
        path_input = 'input.csv'
        path_output = 'output.csv'

        # Cria o arquivo de entrada 
        data = {
            'A': [1, 2, 3]
        }
        df = pd.DataFrame(data)
        df.to_csv(path_input, index=False)

        cleaning.load_data(path_input, path_output, verbose=False)

        # Verifica se o arquivo de saída existe
        self.assertTrue(os.path.exists(path_output))

        # Remove os  arquivos criados
        os.remove(path_input)
        os.remove(path_output)


if __name__ == "__main__":
    unittest.main()