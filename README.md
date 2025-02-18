# Dashboard Mega-Sena - Aplicativo Streamlit

## Visão Geral
Este repositório contém um aplicativo web interativo desenvolvido com **Streamlit** para análise de dados
históricos da Mega-Sena, a principal loteria do Brasil. O aplicativo permite explorar tendências e estatísticas
relacionadas à frequência dos números sorteados, evolução dos prêmios e distribuição de ganhadores em diferentes
categorias (6, 5 e 4 acertos).

### Principais Funcionalidades
- **Filtros Interativos**: Selecione intervalos de anos e números específicos para análise.
- **Análise de Frequência**: Visualize a frequência dos números sorteados (valores absolutos ou percentuais).
- **Evolução dos Prêmios**: Acompanhe a evolução histórica dos valores dos prêmios ao longo dos anos.
- **Distribuição de Ganhadores**: Analise a quantidade de ganhadores por categoria (6, 5 ou 4 acertos) conforme os
filtros aplicados.

## Requisitos
Para executar este aplicativo localmente, é necessário instalar os seguintes pacotes Python:

```bash
pip install streamlit pandas plotly
```

## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/dashboard-mega-sena.git
   cd dashboard-mega-sena


3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

## Estrutura do Aplicativo

### Barra Lateral
A barra lateral contém os seguintes controles interativos:
- Filtro de Ano: Selecione o intervalo de anos para os sorteios da Mega-Sena.
- Filtro de Números Sorteados: Escolha números específicos para filtrar os sorteios.
- Agregação de Prêmios: Opte por somar ou calcular a média dos prêmios.
- Distribuição de Ganhadores: Visualize o número de ganhadores em cada categoria.


## Dados Fonte
O projeto utiliza dados históricos da Mega-Sena, incluindo informações sobre:
- Números sorteados
- Valores dos prêmios
- Frequência de ganhadores em cada categoria