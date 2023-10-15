# Análise de dados

Vamos analisar a relação entre a região e a qualidade da assistência pré-natal. Para isso, precisaremos dos dados de local de nascimento, número de consultas pré-natal e do índice Kotelchuck de qualidade do pré-natal. Isso nos permitirá realizar uma análise tanto quantitativa quanto qualitativa.

## Número de consulta pré-natal por região

Vamos começar pela análise quantitativa, onde examinaremos a distribuição do número de consultas de pré-natal por região no Brasil.

A tabela abaixo mostra a distribuição dos dados:

![](data_analise\average_region.CONSPRENAT.csv)

Podemos notar que, na região Norte, o número médio de consultas pré-natal realizadas por uma mãe é menor que a média encontrada nas regiões Nordeste, Sudeste e Centro-Oeste. Por outro lado, na região Sul, a média é superior em relação às demais regiões. É interessante observar que, em média, uma mãe na região Sul realiza aproximadamente duas consultas a mais de pré-natal do que uma mãe na região Norte. 
Podemos então plotar esses dados para ter uma melhor visualização dos dados.

![](data_analise\images\bar_plot_region.png)

Vamos agora fazer uma análise dos mesmos dados, porém agora com o auxílio de um BoxPlot.

![](data_analise\images\boxplot_region.png)

Vemos que o número de consultas pré-natal de cada mãe é mais concentrado no Sudeste e também que a mediana está acima do meio da caixa do quartil, isso pode indicar que a maioria das mães nessa região tende a fazer um número maior de consultas em comparação com a mediana, o que significa que há um grupo menor de mães que faz menos consultas. 
Os bigodes dos gráficos de caixa estendendo-se até 0 nas regiões Norte, Nordeste e Centro-Oeste indicam que existem mães nessas regiões que não realizam nenhuma consulta de pré-natal. Isso não é considerado atípico, já que é uma parte da distribuição de dados nessas regiões. No entanto, essa observação pode levantar preocupações sobre o acesso aos serviços de saúde e a conscientização sobre a importância do pré-natal nessas áreas.

## Qualidade de consulta pré-natal por região

Vamos agora fazer uma análise qualitativa por região, para isso iremos considerar o índice Kotelchuck. O índice Kotelchuck é uma medida que avalia a qualidade do cuidado pré-natal com base no número e na qualidade das consultas de pré-natal realizadas por uma gestante.

![](data_analise\images\heatmap.png)

Com esse mapa de calor podemos ver claramente que a distribuição da qualidade do pré-natal está relacionada às regiões de nascimentos no Brasil. Ou seja, a qualidade dos serviços prestados é maior no Sul e no Sudeste, enquanto a mesma se encontra bem abaixo dos padrões no Norte.


[Voltar](../README.md)