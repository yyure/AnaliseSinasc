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

# Imagem 1: Gráfico de Barras para Regiões (CONSPRENAT)
output_path_consprenat = 'data_analise/images/bar_plot_region.png'
generate_bar(region_data, column_name1, "Regiões", "Média de CONSPRENAT", "Média de CONSPRENAT por Região", output_path_consprenat)

# Imagem 2: Boxplot para Regiões (CONSPRENAT)
output_path_kotelchuck = 'data_analise/images/boxplot_region.png'
generate_boxplot(region_data, column_name1, "Regiões", "CONSPRENAT", "Distribuição de CONSPRENAT por Região", output_path_kotelchuck)

# Teste 3: Mapa de calor cpara estados (KOTELCHUCK)
output_path_heatmap = 'data_analise/images/heatmap.png'
generate_heatmap(state_data, column_name1, shapefile_path, output_path_heatmap)
