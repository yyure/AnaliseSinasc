# Metodologia

Escolhemos a base de dados SINASC devido a relevância que o monitoramento dos nascimentos tem em toda sociedade, podendo contribuir para o conhecimento da situação de saúde de uma população e para a avaliação de políticas e ações de vigilância e atenção à saúde na área da saúde materno-infantil.

## Os dados

O Sistema de Informações sobre Nascidos Vivos ([SISNAC](https://www.gov.br/saude/pt-br/composicao/svsa/vigilancia-de-doencas-cronicas-nao-transmissiveis/sistemas-de-informacao-em-saude)) foi implantado oficialmente a partir de 1990, com o objetivo de coletar dados sobre os nascimentos ocorridos em todo o território nacional e fornecer informações sobre natalidade para todos os níveis do Sistema de Saúde. Estima-se que a partir de 2011 ele já tenha alcançado 100% da cobertura dos nascidos vivos prevista pelo [IBGE](http://tabnet.datasus.gov.br/cgi/sinasc/Consolida_Sinasc_2011.pdf) e, do momento da realização do trabalho, os anos de 2022 e 2023 ainda estavam em situação de prévia - por isto optamos pelo ano de 2021.

O documento padrão obrigatório em todo território nacional e utilizado para a coleta de dados é a Declaração de Nascidos Vivos (DN), preenchidas pelos profissionais de saúde e recolhidas, regularmente, pelas Secretarias Municipais de Saúde. Nas Secretarias Municipais de Saúde, as DN são digitadas, processadas, criticadas e consolidadas no SINASC local. Em seguida, os dados informados pelos municípios sobre os nascimentos no nível local são transferidos à base de dados do nível estadual que os agrega e os envia ao nível federal.

Lá, o Ministério da Saúde trata da análise, avaliação e distribuição das informações sobre o SINASC, agregando-as por Unidade da Federação, e elaborando relatórios analíticos, painéis de indicadores e outros instrumentos estatísticos de informações sobre natalidade que são disseminados para todo o país.

## Critérios de limpeza

Dado o fato dos dados possivelmente abrangerem toda a população dos nascidos vivos de cada ano, e portanto podermos observar muitos outliers em cada categoria, optou-se por uma limpeza mais conservadora por não conseguirmos afirmar, categoricamente, o que é ou não caso extremo ou simplesmente erro de coleta.

Colunas repetidas e informações menores que julgamos não necessárias para as análises foram removidas, juntamente com qualquer dado que estivesse em branco. Exceções feitas foi quando preenchemos estes valores com 0, no caso da quantidade de gestações anteriores, por exemplo, ou 9 (pergunta ignorada, de acordo com o [dicionário dos dados](https://diaad.s3.sa-east-1.amazonaws.com/sinasc/SINASC+-+Estrutura.pdf)), no caso do tipo da gravidez.

Restrigimos algumas colunas categóricas apenas aos seus possíveis valores de preenchimento (geralmente de 1 a 5), e algumas variáveis quantitativas também foram filtradas pelo Z Score maior que 4 ou menor que -4.

Posteriormente, já no contexto dos objetivos de cada análise, foram utilizadas apenas as colunas julgadas pertinentes e que resultam na visualização final.

## Abordagem analítica

A priori cada membro explorou os dados individualmente e então dividiu-se o trabalho por temática de forma que não se conflitasse muito entre as escolhas. Para não deixar de abordar os dados em toda sua completude, toda análise complementa as demais pois tratam, essencialmente, do mesmo assunto em diferentes níveis e recortes.

Depois de feito o módulo de limpeza de maneira conjunta e seu push para a main, cada membro teve sua própria branch para trabalho e, apenas após concluída boa parte de sua análise, dava-se push para a branch de desenvolvimento. No decorrer do tempo foram feitos merges para ajustar cada análise e manter os modulos funcionais, concluindo-se com o push final para a main.

Num geral, foi dado mais enfâse nas descobertas que cada membro obteve de sua exploração dos dados e, no processo, ao seu aprendizado das ferramentas Pandas e Matplotlib. Disto resulta que não procuramos seguir o rigor estatístico e nem demos enfâse excessiva nas visualizações, justamente por acreditarmos não ser esse o foco do trabalho.