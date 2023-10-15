import pandas as pd
import analysis
from visualization import generate_bar, generate_boxplot, generate_heatmap
from data_analise.mapping import region_mapping, state_mapping

# Caminho para o arquivo CSV inicial
csv_file_path = "../data/saida.csv"

# Caminho para o shapefile
shapefile_path = "data_analise/shapefile/estados_2010.shp"

# Colunas para as visualizações
column_name1 = "KOTELCHUCK"
column_name2 = "CONSPRENAT"

df = pd.read_csv(csv_file_path, encoding="unicode_escape", engine="python", sep=";")
df = df[["CODMUNNASC", column_name1, column_name2]]

# Separa o DataFrame por estado e região
state_data = analysis.separate_by_location(df, state_mapping)
region_data = analysis.separate_by_location(df, region_mapping)

# Tabela das médias (CONSPRENAT)
analysis.calculate_and_save_region_averages(region_data, column_name2, "data_analise/average_region.CONSPRENAT.csv")

# Imagem 1: Gráfico de Barras para Regiões (CONSPRENAT)
output_path_1 = 'data_analise/images/bar_plot_region.png'
generate_bar(region_data, column_name2, "Regiões", f"Média de {column_name2} por Região", output_path_1)

# Imagem 2: Boxplot para Regiões (CONSPRENAT)
output_path_2 = 'data_analise/images/boxplot_region.png'
generate_boxplot(region_data, column_name2, "Regiões", f"Distribuição de {column_name2} por Região", output_path_2, 20)

# Teste 3: Mapa de calor cpara estados (KOTELCHUCK)
output_path_3 = 'data_analise/images/heatmap.png'
generate_heatmap(state_data, column_name1, shapefile_path, output_path_3)