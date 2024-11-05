import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from model_service import model_predict
from pipeline_service import run_pipeline

# Removendo o espaço superior e organizando o layout
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;  
    }
    .stTitle {
        line-height: 1.0;  
    }
    </style>
    """, unsafe_allow_html=True
)

# Título em uma linha
st.title("💧 Monitoramento de fraudes no consumo de água")

# Aba com espaçamento mais compacto
tabs = st.tabs(["Geral", "Raw Data"])

# Inicializando o filtro de categoria
with tabs[0]:
    # Sidebar
    with st.sidebar:
        st.header("Adicione o CSV")
        dash_file = st.file_uploader("Limite de 500MB", type=["csv"])

        st.header("Filtre por")
        
        categoria_selecionada = st.selectbox("Categoria", options=["Todos", "Residencial", "Comercial", "Industrial", "Público"])

    if dash_file is not None:
        df_original = pd.read_csv(dash_file, sep=',')

        df_original['DAT_LEITURA'] = pd.to_datetime(df_original['DAT_LEITURA'], dayfirst=True, errors='coerce')

        # Rodando o pipeline e as previsões 
        df_dash = run_pipeline(df_original)
        df_dash = model_predict(df_dash)

        # Realizando o merge com as colunas adicionais necessarias para analise
        df_dash = df_dash.merge(
            df_original[['MATRICULA', 'COD_ROTA_LEITURA', 'COD_LATITUDE', 'COD_LONGITUDE']], 
            on='MATRICULA', 
            how='right'
        )
        df_dash = df_dash.drop_duplicates(subset='MATRICULA')

        # Filtrando pela categoria selecionada 
        if categoria_selecionada == "Residencial":
            df_dash = df_dash[df_dash['ECO_RESIDENCIAL'] == 1]
        elif categoria_selecionada == "Comercial":
            df_dash = df_dash[df_dash['ECO_COMERCIAL'] == 1]
        elif categoria_selecionada == "Industrial":
            df_dash = df_dash[df_dash['ECO_INDUSTRIAL'] == 1]
        elif categoria_selecionada == "Público":
            df_dash = df_dash[df_dash['ECO_PUBLICA'] == 1]


    else:
        st.warning("Por favor, carregue um arquivo CSV.")

    # Layout principal com duas colunas
    col1, col2 = st.columns(2)
    col1, col_spacer, col2 = st.columns([1.5, 0.3, 1])

with col1:
    st.markdown("<p style=' font-size:1.5em; margin-top: 10px;'>Volume consumido medido em localidades fraudadoras</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:gray; font-size:0.9em; margin-top: -15px;'>Os dados de localidade não foram usados no modelo de identificação de fraudes e representam o bairro, garantindo a confidencialidade dos consumidores</p>", unsafe_allow_html=True)

    # Filtrando o DataFrame para apenas as previsões fraudulentas
    if dash_file is not None and 'Predictions' in df_dash.columns:
        df_fraudulentas = df_dash[df_dash['Predictions'] == 1]

        # Criando a coluna 'Categoria' com base nas colunas binárias
        def definir_categoria(row):
            if row['ECO_RESIDENCIAL'] == 1:
                return 'Residencial'
            elif row['ECO_COMERCIAL'] == 1:
                return 'Comercial'
            elif row['ECO_INDUSTRIAL'] == 1:
                return 'Industrial'
            elif row['ECO_PUBLICA'] == 1:
                return 'Público'
            else:
                return 'Não Definido'

        df_fraudulentas['Categoria'] = df_fraudulentas.apply(definir_categoria, axis=1)

        # Calculando o volume como a soma das colunas de consumo
        df_fraudulentas['Volume'] = df_fraudulentas[['CONS_MEDIDO_M-0', 'CONS_MEDIDO_M-1', 'CONS_MEDIDO_M-2', 'CONS_MEDIDO_M-3', 'CONS_MEDIDO_M-4']].sum(axis=1)

        # Definindo as cores para cada categoria

        color_map = {
            'Residencial': '#2D2FA6',  # Azul
            'Comercial': '#0D0E34',    # Azul escuro
            'Industrial': '#1E89CC',   # Ciano
            'Público': '#41ECFF'        # Azul claro
        }

        # Criando o DataFrame para o mapa, usando latitude e longitude reais
        map_data = df_fraudulentas[['COD_LATITUDE', 'COD_LONGITUDE', 'Categoria', 'Volume']].rename(columns={
            'COD_LATITUDE': 'lat',
            'COD_LONGITUDE': 'lon'
        })

        # Verificando se há dados suficientes para o gráfico
        if not map_data.empty:
            # Mapa com Plotly Express
            fig = px.scatter_mapbox(map_data, lat="lat", lon="lon", size="Volume", color="Categoria",
                                    color_discrete_map=color_map, zoom=10, height=700, width=800)

            # Configuração do layout do mapa
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado fraudulento disponível para exibir no mapa.")
    else:
        pass

with col2:
    st.markdown("<p style='font-size:1.5em; margin-top: 10px;'>Top 5 rotas de leitura fraudadoras por quantidade de matrículas</p>", unsafe_allow_html=True)

    if dash_file is not None and 'Predictions' in df_dash.columns:
        # Filtrando o df_dash para apenas as previsões iguais a 1
        df_fraudulentas = df_dash[df_dash['Predictions'] == 1]

        # Agrupando os dados por rota de leitura e contando as matrículas
        rota_data = df_fraudulentas['COD_ROTA_LEITURA'].value_counts().reset_index()
        rota_data.columns = ['Rota de Leitura', 'Quantidade']  

        # Selecionando as 5 rotas de leitura com maior quantidade
        top_rotas = rota_data.nlargest(5, 'Quantidade')
        top_rotas['Rota de Leitura'] = top_rotas['Rota de Leitura'].astype(str)

        # Criação do gráfico de barras
        fig = go.Figure(data=go.Bar(
            x=top_rotas['Rota de Leitura'],  
            y=top_rotas['Quantidade'],
            marker=dict(color='royalblue')  
        ))

        fig.update_layout(
            title="Top 5 Rotas de Leitura Fraudadoras",
            xaxis_title="Rota de Leitura",
            yaxis_title="Quantidade de fraudes",
            xaxis=dict(type='category'),  
            margin=dict(t=40, b=20),  
            height=250
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        pass

with col2:
    st.subheader("Matrículas fraudadoras por rota de leitura")
    rota_filtro = st.text_input("Filtre por rota de leitura")

    # Filtrando o df_dash para apenas as previsões iguais a fraude
    if dash_file is not None:
        df_fraudulentas = df_dash[df_dash['Predictions'] == 1]

        # Aplicando filtro
        if rota_filtro.strip():  
            try:
                rota_filtro_num = int(rota_filtro)  
                df_fraudulentas = df_fraudulentas[df_fraudulentas['COD_ROTA_LEITURA'] == rota_filtro_num]
            except ValueError:
                st.warning("Por favor, insira um número válido para a rota de leitura.")  

        # Criação do DataFrame para exibição 
        matriculas_data = df_fraudulentas[['MATRICULA', 'COD_ROTA_LEITURA']].rename(columns={
            'MATRICULA': 'Matrícula',
            'COD_ROTA_LEITURA': 'Rota de Leitura'
        })
        
        # Checkbox para controlar a visibilidade das matrículas
        show_matriculas = st.checkbox('👁️ Mostrar Matrículas', value=False)

        # Aplica a máscara se o checkbox estiver desativado
        if not show_matriculas:
            matriculas_data['Matrícula'] = matriculas_data['Matrícula'].apply(lambda x: '*****')  

        # Exibição da tabela de matrículas
        st.dataframe(matriculas_data)


# Aba "Raw Data" para dados brutos
with tabs[1]:
    st.header("Raw Data")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        
        #lendo csv
        df = pd.read_csv(uploaded_file, sep=',')
        
        #passando dados pela pipe
        df = run_pipeline(df)
        
        #passando pelo modelo
        df = model_predict(df)
        
        st.write("Visualização do CSV:")
        st.dataframe(df)  
        
    else:
        st.write("Por favor, faça o upload de um arquivo CSV.")