import unittest
import pandas as pd
import pandas.testing as pd_testing
import os

from data.mapping import return_region, return_state
import analysis

class TestAnalysis(unittest.TestCase):
    def assertDataFrameEqual(self, a, b, msg):
        try:
            pd_testing.assert_frame_equal(a, b)
        except AssertionError as e:
            raise self.failureException(msg) from e
    
    def setUp(self):
        self.addTypeEqualityFunc(pd.DataFrame, self.assertDataFrameEqual)

    # Teste 1: Função separate_by_location - Exceção para mapping invalido
    def test_invalid_mapping(self):
        df = pd.DataFrame({
            'CODMUNNASC': ['12876', '275342', '53342'],
            'KOTELCHUCK': [10, 20, 30],
            'CONSPRENAT': [5, 8, 6]
        })

        invalid_mapping = {
            '12': 'Acre',
            '13': 'Amazonas'
        }

        with self.assertRaises(ValueError):
            analysis.separate_by_location(df, invalid_mapping)

    # Teste 2: Função eparate_by_location - Teste com o dicionário de regiões (O codigo do Norte é 1)
    def test_region_mapping(self):
        df = pd.DataFrame({
            'CODMUNNASC': ['120001', '270002', '530003', '111111'],
            'KOTELCHUCK': [10, 20, 30, 40],
            'CONSPRENAT': [5, 8, 6, 7]
        })

        region_mapping = return_region()
        result = analysis.separate_by_location(df, region_mapping)

        # Verifica um item do dicionário
        self.assertTrue("Norte" in result)
        self.assertEqual(result["Norte"].shape[0], 2)

        # Verifica se tem as colunas esperadas
        self.assertTrue("CODMUNNASC" in result["Norte"].columns)
        self.assertTrue("KOTELCHUCK" in result["Norte"].columns)
        self.assertTrue("CONSPRENAT" in result["Norte"].columns)

    # Teste 3: Função eparate_by_location - Teste do dicionário de estados (O codigo do Acre é 12)
    def test_separate_by_location_state_mapping(self):
        df = pd.DataFrame({
            'CODMUNNASC': ['120001', '270002', '530003'],
            'KOTELCHUCK': [10, 20, 30],
            'CONSPRENAT': [5, 8, 6]
        })

        region_mapping = return_state()
        result = analysis.separate_by_location(df, region_mapping)

        # Verifica um item do dicionário
        self.assertTrue("Acre" in result)
        self.assertEqual(result["Acre"].shape[0], 1)

        # Verifica valores de uma linha de um item
        self.assertEqual(result["Acre"]["CODMUNNASC"].iloc[0], '12')
        self.assertEqual(result["Acre"]["KOTELCHUCK"].iloc[0], 10)
        self.assertEqual(result["Acre"]["CONSPRENAT"].iloc[0], 5)

    # Teste 4: Função calculate_and_save_region_averages - Exceção para coluna inexistente em DataFrame
    def test_invalid_column(self):
        df = {
            'Acre': pd.DataFrame({
                'CODMUNNASC': ['12'],
                'KOTELCHUCK': [10],
                'CONSPRENAT': [1]
            }),
            'Amazonas': pd.DataFrame({
                'CODMUNNASC': ['27'],
                'KOTELCHUCK': [20],
                'CONSPRENAT': [1]
            })}

        with self.assertRaises(ValueError):
            analysis.calculate_and_save_region_averages(df, "Invalid_Column", "average.csv")

    # Teste 5: Função calculate_and_save_region_averages - Exceção para dicionário vazio
    def test_empty_dict2(self):
        data_dict = pd.DataFrame({})

        with self.assertRaises(ValueError):
            analysis.calculate_and_save_region_averages(data_dict, 'INVALID_COLUMN', 'averages.csv')

    # Teste 6: Função calculate_and_save_region_averages - Exceção para output_path invalido
    def test_invalid_output_path(self):
        df = {
            'Acre': pd.DataFrame({
                'CODMUNNASC': ['12'],
                'KOTELCHUCK': [10],
                'CONSPRENAT': [1]
            }),
            'Amazonas': pd.DataFrame({
                'CODMUNNASC': ['27'],
                'KOTELCHUCK': [20],
                'CONSPRENAT': [1]
            })}

        with self.assertRaises(FileNotFoundError):
            analysis.calculate_and_save_region_averages(df, 'CONSPRENAT', '')

    # Teste 7: Função calculate_and_save_region_averages
    def test_calculate_and_save_region_averages(self):
        df = {
            'Acre': pd.DataFrame({
                'CODMUNNASC': ['12'],
                'KOTELCHUCK': [10],
                'CONSPRENAT': [1]
            }),
            'Amazonas': pd.DataFrame({
                'CODMUNNASC': ['27'],
                'KOTELCHUCK': [20],
                'CONSPRENAT': [1]
            })}
        
        analysis.calculate_and_save_region_averages(df, "CONSPRENAT", "average.csv")

        # Verifica se o arquivo CSV foi criado
        self.assertTrue(os.path.isfile("average.csv"))

        averages_df = pd.read_csv("average.csv", sep=";")
        
        # Verifica se o arquivo CSV tem as colunas esperadas
        expected_columns = ["DataFrame", "Soma Total", "Total de Nascimentos", "Média"]
        self.assertListEqual(list(averages_df.columns), expected_columns)

        os.remove('average.csv')

if __name__ == '__main__':
    unittest.main(buffer=True)
