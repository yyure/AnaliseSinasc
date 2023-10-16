import unittest
import pandas as pd
import pandas.testing as pd_testing
import numpy as np

import statics

class TestStatics(unittest.TestCase):
    def assertDataFrameEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e
    
    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataFrameEqual)
    
    # Teste 1: Função recebe parâmetros adequados para n=1
    def test_fr_relativa_aux_input_1(self):
        df = pd.DataFrame({
            'Dados': [1, 1, 3, 1, 5]
        })
        n = 1
        i = 1
        j = 5
        column = 'Dados'

        result = statics.fr_relativa_aux(df, column, n, i, j)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1', '2', '3', '4', '5'],
            'freq. relativa': [0.6, 0.0, 0.2, 0.0, 0.2]
        })

        self.assertEqual(result, expected)

    # Teste 2: Função recebe parâmetros adequados para n!=1
    def test_fr_relativa_aux_input_n(self):
        df = pd.DataFrame({
            'Dados': [1, 1, 3, 1, 5]
        })
        n = 3
        i = 1
        j = 5
        column = 'Dados'

        result = statics.fr_relativa_aux(df, column, n, i, j)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1 a 4', '4 a 7', '7 a 10'],
            'freq. relativa': [0.8, 0.2, 0.0]
        })

        self.assertEqual(result, expected)

    # Teste 3: Função recebe DataFrame vazio
    def test_fr_relativa_aux_empty(self):
        with self.assertRaises(ValueError):
            df = pd.DataFrame()
            n = 3
            i = 1
            j = 5
            column = 'Dados'

            statics.fr_relativa_aux(df, column, n, i, j)

    # Teste 4: Função recebe coluna inválida e/ou não presente no DataFrame 
    def test_fr_relativa_aux_column(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({
                'Dados 1': [1, 2, 0, 0]
                })
            n = 3
            i = 1
            j = 5
            column = 'Dados'

            statics.fr_relativa_aux(df, column, n, i, j)

    # Teste 5: Função recebe parâmetros adequados para n=1
    def test_fr_relativa_input_1(self):
        df = pd.DataFrame({
            'Dados': [1, 1, 3, 1, 5]
        })
        n = 1
        column = 'Dados'

        result = statics.fr_relativa(df, column, n)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1', '2', '3', '4', '5'],
            'freq. relativa': [0.6, 0.0, 0.2, 0.0, 0.2]
        })

        self.assertEqual(result, expected)

    # Teste 6: Função recebe parâmetros adequados para n!=1
    def test_fr_relativa_input_n(self):
        df = pd.DataFrame({
            'Dados': [1, 1, 3, 1, 5]
        })
        n = 3
        column = 'Dados'

        result = statics.fr_relativa(df, column, n)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1 a 4', '4 a 7', '7 a 10'],
            'freq. relativa': [0.8, 0.2, 0.0]
        })

        self.assertEqual(result, expected)

    # Teste 7: Função recebe DataFrame vazio
    def test_fr_relativa_empty(self):
        with self.assertRaises(ValueError):
            df = pd.DataFrame()
            n = 3
            column = 'Dados'

            statics.fr_relativa(df, column, n)

    # Teste 8: Função recebe coluna inválida e/ou não presente no DataFrame
    def test_fr_relativa_column(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({'Dados 1': [1, 2, 0, 0]})
            n = 3
            column = 'Dados'

            statics.fr_relativa(df, column, n)

    # Teste 9: Função recebe parâmetros adequados para n=1
    def test_frelat_ufs_input_1(self):
        df = pd.DataFrame({
            'UF': [13, 33, 13, 35 ,13, 35, 13, 13],
            'Dados': [3, 5, 3, 1, 3, 6, 2, 2]
            })
        n = 1
        cod_uf = 'UF'
        column = 'Dados'

        result = statics.frelat_ufs(df, cod_uf, column, n)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1', '2', '3', '4', '5', '6'],
            'AM fri.': [0.0, 0.4, 0.6, 0.0, 0.0, 0.0],
            'RJ fri.': [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            'SP fri.': [0.5, 0.0, 0.0, 0.0, 0.0, 0.5]
        })

        self.assertEqual(result, expected)

    # Teste 10: Função recebe parâmetros adequados para n!=1
    def test_frelat_ufs_input_n(self):
        df = pd.DataFrame({
            'UF': [13, 33, 13, 35 ,13, 35, 13, 13],
            'Dados': [3, 5, 3, 1, 3, 6, 2, 2]
            })
        n = 3
        cod_uf = 'UF'
        column = 'Dados'

        result = statics.frelat_ufs(df, cod_uf, column, n)

        # Retorno esperado da função
        expected = pd.DataFrame({
            'Dados': ['1 a 4', '4 a 7', '7 a 10'],
            'AM fri.': [1.0, 0.0, 0.0],
            'RJ fri.': [0.0, 1.0, 0.0],
            'SP fri.': [0.5, 0.5, 0.0]
        })

        self.assertEqual(result, expected)

    # Teste 11: Função recebe DataFrame vazio
    def test_frelat_ufs_empty(self):
        with self.assertRaises(ValueError):
            df = pd.DataFrame()
            n = 3
            cod_uf = 'Estados'
            column = 'Dados'

            statics.frelat_ufs(df, cod_uf, column, n)

    # Teste 12: Função recebe coluna inválida e/ou não presente no DataFrame
    def test_frelat_ufs_column(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({
                'Dados 1': [1, 2, 0, 0],
                'Estados': [12, 17, 12, 11]
                })
            n = 3
            cod_uf = 'Estados'
            column = 'Dados'

            statics.frelat_ufs(df, cod_uf, column, n)

    # Teste 13: Função recebe coluna de códigos UF não existente
    def test_frelat_ufs_uf(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({
                'Dados': [1, 2, 0, 0],
                'Estados': [12, 17, 12, 11]
                })
            n = 3
            cod_uf = 'Estadas'
            column = 'Dados'

            statics.frelat_ufs(df, cod_uf, column, n)

    # Teste 14: Função recebe parâmetros adequados
    def test_filter_uf(self):
        df = pd.DataFrame({
                'UF': [13, 33, 13, 35 ,13, 35, 13, 13],
                'Dados 1': [3, 5, 3, 1, 3, 6, 2, 2],
                'Dados 2': [1, 3, 3, 1, 0, 5, 0, 1]
            })
        cod_uf = 'UF'
        dados = ['Dados 1', 'Dados 2']

        result = statics.filter_uf(df, cod_uf, dados)

        # Retorno esperado da função
        expected = {
            'AM': pd.DataFrame({
                'Dados 1': [5.0, 2.6, 0.547723, 2.0, 2.0, 3.0, 3.0, 3.0],
                'Dados 2': [5.0, 1.0, 1.224745, 0.0, 0.0, 1.0, 1.0, 3.0]
            }, index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']),
            'RJ': pd.DataFrame({
                'Dados 1': [1.0, 5.0, None, 5.0, 5.0, 5.0, 5.0, 5.0],
                'Dados 2': [1.0, 3.0, None, 3.0, 3.0, 3.0, 3.0, 3.0]
            }, index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']),
            'SP': pd.DataFrame({
                'Dados 1': [2.0, 3.5, 3.535534, 1.0, 2.25, 3.5, 4.75, 6.0],
                'Dados 2': [2.0, 3.0, 2.828427, 1.0, 2.0, 3.0, 4.0, 5.0]
            }, index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
        }

        # Conversão dos resultados para facilitamento do assert
        expected_list = list(expected)
        result_list = list(result)

        self.assertEqual(result_list, expected_list)

    # Teste 15: Função recebe coluna de códigos UF não existente
    def test_filter_uf_uf(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({
                'UF': [13, 33, 13, 35 ,13, 35, 13, 13],
                'Dados 1': [3, 5, 3, 1, 3, 6, 2, 2],
                'Dados 2': [1, 3, 3, 1, 0, 5, 0, 1]
            })
            cod_uf = 'Estados'
            dados = ['Dados 1', 'Dados 2']

            result = statics.filter_uf(df, cod_uf, dados)        

    # Teste 16: Função recebe coluna inválida e/ou não presente no DataFrame
    def test_filter_uf_column(self):
        with self.assertRaises(KeyError):
            df = pd.DataFrame({
                'UF': [13, 33, 13, 35 ,13, 35, 13, 13],
                'Dados 1': [3, 5, 3, 1, 3, 6, 2, 2],
                'Dados 2': [1, 3, 3, 1, 0, 5, 0, 1]
            })
            cod_uf = 'UF'
            dados = ['Dados', 'Dados 2']

            statics.filter_uf(df, cod_uf, dados) 

if __name__ == '__main__':
    unittest.main(buffer=True)