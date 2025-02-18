import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():

    df = pd.read_excel('assets/Mega-Sena.xlsx')
    df['Data do Sorteio'] = pd.to_datetime(df['Data do Sorteio'], errors='coerce')
    df = df.dropna(subset=['Data do Sorteio'])

    for i in range(1, 7):
        df[f'Bola{i}'] = pd.to_numeric(df[f'Bola{i}'], errors='coerce')
    return df

def limpa_string(x):
    
    """
    Limpa strings de valores monetários:
      - Remove o símbolo "R$" e espaços
      - Remove o separador de milhares (ponto)
      - Substitui a vírgula decimal por ponto
    Se o valor não for string, retorna o valor inalterado.
    """
    if isinstance(x, str):
        x = x.replace('R$', '').strip()
        x = x.replace('.', '')
        x = x.replace(',', '.')
    return x

df = load_data()

st.image("assets/mega-sena-logo.png")
st.title("Dashboard Mega-Sena")

# --- Sidebar ---
st.sidebar.image("assets/images.png")
st.sidebar.header("Filtros Básicos")
st.sidebar.subheader("Controles Globais")

# Filtro por intervalo de anos
anos = sorted(df['Data do Sorteio'].dt.year.dropna().unique())
ano_inicial, ano_final = st.sidebar.select_slider(
    'Selecione o intervalo de anos:',
    options=anos,
    value=(min(anos), max(anos))
)

# Filtro: Seleção de números sorteados
numero_escolhido = st.sidebar.multiselect("Selecione números de bolas para filtrar:", list(range(1, 61)))


df_filtrado = df[(df['Data do Sorteio'].dt.year >= ano_inicial) &
                 (df['Data do Sorteio'].dt.year <= ano_final)]

# Filtro: registros onde pelo menos uma das bolas tenha o valor selecionado
if numero_escolhido:
    df_filtrado = df_filtrado[
        df_filtrado.apply(
            lambda row: any(row[f'Bola{i}'] in numero_escolhido for i in range(1, 7)),
            axis=1
        )
    ]

# --- Widgets ---
st.sidebar.header("Controles Específicos")
st.sidebar.subheader("Valor de prêmios")

# Widget 1: Modo de exibição da frequência (Gráfico 1)
display_mode = st.sidebar.radio("Exibir frequência como:", options=["Absoluto", "Percentual"], index=0)

# Widget 2: Método de agregação dos prêmios (Gráfico 2)
aggregation_method = st.sidebar.selectbox("Agregação dos Prêmios:", options=["Soma", "Média"])

st.sidebar.subheader("Acertos da vitoria")

# Widget 3: Categorias de ganhadores a exibir (Gráfico 3)
categories_to_display = st.sidebar.multiselect(
    "Filtro por acertos:",
    options=["6 acertos", "5 acertos", "4 acertos"],
    default=["6 acertos", "5 acertos", "4 acertos"]
)

# --- Gráfico 1: Frequência dos Números Sorteados ---
st.subheader("Frequência dos Números Sorteados")
numeros = []
for i in range(1, 7):
    numeros.extend(df_filtrado[f'Bola{i}'].dropna().tolist())
freq = pd.Series(numeros).value_counts().sort_index()

if freq.empty:
    st.warning("Nenhum registro encontrado para o filtro selecionado.")
else:
    if display_mode == "Percentual":
        total = freq.sum()
        freq = (freq / total * 100).round(2)
        y_label = "Frequência (%)"
    else:
        y_label = "Frequência"

    fig_freq = px.bar(
        x=freq.index,
        y=freq.values,
        labels={'x': 'Número', 'y': y_label},
        title="Frequência dos Números (1 a 60)",
        color_discrete_sequence=['#28a745']
    )
    st.plotly_chart(fig_freq)

# --- Gráfico 2: Evolução historica do valor de prêmios ---
st.subheader("Evolução historica do valor de prêmios")
df_filtrado['Rateio 6 acertos'] = df_filtrado['Rateio 6 acertos'].apply(limpa_string)
df_filtrado['Rateio 6 acertos'] = pd.to_numeric(df_filtrado['Rateio 6 acertos'], errors='coerce')

# Agrega os prêmios por ano de acordo com o método selecionado
agrupado = df_filtrado.groupby(df_filtrado['Data do Sorteio'].dt.year)['Rateio 6 acertos']
if aggregation_method == "Soma":
    premio_por_ano = agrupado.sum().reset_index()
else:  # Média
    premio_por_ano = agrupado.mean().reset_index()

premio_por_ano.columns = ['Ano', 'Prêmio']

if premio_por_ano.empty:
    st.warning("Não há dados para evoluir os prêmios com o filtro aplicado.")
else:
    fig_premio = px.line(
        premio_por_ano,
        x='Ano',
        y='Prêmio',
        labels={'Ano': 'Ano', 'Prêmio': 'Prêmio'},
        title=f"Evolução dos Prêmios ({aggregation_method})",
        line_shape="linear",
        markers=True,
        color_discrete_sequence=['#28a745'] 
    )
    st.plotly_chart(fig_premio)

# --- Gráfico 3: Distribuição de Ganhadores por Categoria ---
st.subheader("Distribuição de Ganhadores por Categoria")
dados_cat = {
    '6 acertos': df_filtrado['Ganhadores 6 acertos'].sum(),
    '5 acertos': df_filtrado['Ganhadores 5 acertos'].sum(),
    '4 acertos': df_filtrado['Ganhadores 4 acertos'].sum()
}

# Filtra apenas as categorias selecionadas pelo usuário
dados_cat = {cat: valor for cat, valor in dados_cat.items() if cat in categories_to_display}

# Verifica se há dados para exibir
if not dados_cat:
    st.warning("Nenhuma categoria selecionada ou sem dados para exibir.")
else:
    # Cria um DataFrame para o gráfico
    categoria_contagem = pd.DataFrame(list(dados_cat.items()), columns=['Categoria', 'Contagem'])

    # Verifica se o DataFrame está vazio
    if categoria_contagem.empty or categoria_contagem['Contagem'].sum() == 0:
        st.warning("Não há dados para exibir a distribuição de ganhadores com o filtro aplicado.")
    else:
        # Cria o gráfico de pizza
        fig_categoria = px.pie(
            categoria_contagem,
            names='Categoria',
            values='Contagem',
            title="Distribuição de Ganhadores",
            color_discrete_sequence=['#28a745']
        )
        st.plotly_chart(fig_categoria)
