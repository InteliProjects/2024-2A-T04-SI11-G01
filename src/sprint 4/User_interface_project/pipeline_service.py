import pandas as pd
import numpy as np
import re
from datetime import datetime
import gdown
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten, Input, Dropout, BatchNormalization
from tensorflow.keras.metrics import BinaryAccuracy, AUC, Precision, Recall
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical

from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA

def drop_columns(df, column_name):
  df = df.drop(column_name, axis=1)
  return df

def convert_data_types(datasets):
  for column in datasets.select_dtypes(include=['float64', 'int64']).columns:
      if column not in ["COD_LATITUDE", "COD_LONGITUDE"]:
          datasets[column] = datasets[column].astype('Int64')

  # Convert specific object columns to datetime
  if 'REFERENCIA' in datasets.columns:
      datasets['REFERENCIA'] = pd.to_datetime(datasets['REFERENCIA'], errors='coerce')
  if 'DAT_LEITURA' in datasets.columns:
      datasets['DAT_LEITURA'] = pd.to_datetime(datasets['DAT_LEITURA'], errors='coerce')
  return datasets

def padronizar_texto(df, column_name):

  # Cria uma cópia da coluna para evitar modificações no DataFrame original
  new_column = df[column_name].copy()

  # Converte todos os textos para maiúsculas
  new_column = new_column.str.upper()

  # Remove caracteres especiais
  new_column = new_column.apply(lambda x: re.sub(r'[^a-zA-Z0-9]', '', str(x)))

  return new_column

def agrupar_valores(df, column_name):
  df[column_name] = df[column_name].map(lambda x: 'NORMAL' if x == 'NORMAL' else 'ANORMALIDADE')
  return df[column_name] # Return only the modified column

def one_hot_encoding(df, column_name):
  df_encoded = pd.get_dummies(df, columns=[column_name], prefix=[column_name])
  return df_encoded

def categorizar_consumo(df, column_name):


  # Criação novas colunas para as categorias de consumo
  df['Consumo_Alto'] = 0
  df['Consumo_Medio'] = 0
  df['Consumo_Baixo'] = 0

  # Categorizando o consumo
  df.loc[df[column_name] > 0.7, 'Consumo_Alto'] = 1
  df.loc[(df[column_name] >= 0.2) & (df[column_name] <= 0.7), 'Consumo_Medio'] = 1
  df.loc[df[column_name] < 0.2, 'Consumo_Baixo'] = 1

  return df

def normalize_column(df, column_name):

  column_values = df[column_name]

  # Calcula os valores maximos e minimos
  min_value = column_values.min()
  max_value = column_values.max()

  # normaliza o valor
  normalized_values = (column_values - min_value) / (max_value - min_value)

  # retorna a coluna com dados normalizados
  df_normalized = df.copy()
  df_normalized[column_name] = normalized_values

  return df_normalized["CONS_MEDIDO"]

def apply_pca(df_CONSUMO, colunas_features):
  pca = PCA(n_components=3)
  df_CONSUMO[colunas_features] = pca.fit_transform(df_CONSUMO[colunas_features])
  print(f'Variância explicada por cada componente: {pca.explained_variance_ratio_}')

def redimensionar_dataframe(df, coluna_data, coluna_matricula, colunas_features):
    # Converte a coluna de data para datetime
    df[coluna_data] = pd.to_datetime(df[coluna_data])

    # Determina a data mais recente (M) no DataFrame
    data_maxima = df[coluna_data].max()

    # Calcula a data limite (M - 5 meses)
    data_limite = data_maxima - pd.DateOffset(months=5)

    # Filtra o DataFrame para manter apenas as datas no intervalo entre data_limite e data_maxima
    df = df[(df[coluna_data] >= data_limite) & (df[coluna_data] <= data_maxima)]

    # Cria um dicionário para armazenar os dados redimensionados
    dados_redimensionados = {}

    # Identifica as colunas que não estão nas colunas_features
    colunas_estaticas = [col for col in df.columns if col not in colunas_features and col not in [coluna_data, coluna_matricula]]

    # Itera sobre as matrículas únicas
    for matricula in df[coluna_matricula].unique():
        # Filtra o DataFrame para a matrícula atual
        df_matricula = df[df[coluna_matricula] == matricula]

        # Cria um dicionário para armazenar os dados da matrícula atual
        dados_matricula = {coluna_matricula: matricula}

        # Adiciona as colunas estáticas (que não variam com o tempo)
        for coluna in colunas_estaticas:
            dados_matricula[coluna] = df_matricula[coluna].iloc[0]

        # Para cada coluna feature, cria uma nova coluna para cada mês do intervalo
        for coluna in colunas_features:
            for i, data in enumerate(pd.date_range(data_limite, data_maxima, freq='M')):
                # Verifica se a data existe no DataFrame filtrado pela matrícula
                valor = df_matricula.loc[df_matricula[coluna_data].dt.to_period('M') == data.to_period('M'), coluna]

                # Adiciona o valor correspondente, ou 0 se a data não existir
                if not valor.empty:
                    dados_matricula[f"{coluna}_M-{i}"] = valor.iloc[0]
                else:
                    dados_matricula[f"{coluna}_M-{i}"] = 0

        # Adiciona os dados da matrícula ao dicionário principal
        dados_redimensionados[matricula] = dados_matricula

    # Cria um novo DataFrame a partir do dicionário redimensionado
    df_redimensionado = pd.DataFrame.from_dict(dados_redimensionados, orient='index')

    # Substitui todos os NaN por 0 no DataFrame final
    df_redimensionado.fillna(0, inplace=True)

    return df_redimensionado

def pipeline_tratamento(df_CONSUMO, colunas_remover, colunas_normalizar, colunas_padronizar, colunas_agrupamento, colunas_onehot, coluna_consumo, coluna_data, coluna_matricula, colunas_features):
  # A função de parquet foi retirada por enquanto
  # dataset_parquet = transform_load_parquet(dataset)

  for coluna_drop in colunas_remover:
      df_CONSUMO = drop_columns(df_CONSUMO, coluna_drop)

  df_CONSUMO = convert_data_types(df_CONSUMO)

  # Agrupamento de texto
  for coluna in colunas_agrupamento:
    df_CONSUMO[coluna] = agrupar_valores(df_CONSUMO, coluna)


  # Padronização de texto
  for coluna_padrao in colunas_padronizar:
      df_CONSUMO[coluna_padrao] = padronizar_texto(df_CONSUMO, coluna_padrao)

  # One-hot encoding
  for coluna_one in colunas_onehot:
      df_CONSUMO = one_hot_encoding(df_CONSUMO, coluna_one)

  # Criação de categorias de consumo
  df_CONSUMO = categorizar_consumo(df_CONSUMO, coluna_consumo)

  # Normalização
  for coluna_norm in colunas_normalizar:
      df_CONSUMO[coluna_norm] = normalize_column(df_CONSUMO, coluna_norm)

  # PCA features -> melhorar para próxima sprint
  # for coluna_pca in colunas_features:
  #     df_CONSUMO[coluna_pca] = apply_pca(df_CONSUMO, coluna_pca)

  # Redimensionamento do DataFrame
  df_CONSUMO = redimensionar_dataframe(df_CONSUMO, coluna_data, coluna_matricula, colunas_features)

  return df_CONSUMO

def run_pipeline(df):
    df_CONSUMO = df
    colunas_remover =  ['Unnamed: 0','EMP_CODIGO', 'COD_GRUPO', 'COD_SETOR_COMERCIAL', 'ECO_OUTRAS', 'FATURADO_MEDIA', 'COD_LEITURA_INF_1', 'COD_LEITURA_INF_2', 'COD_LEITURA_INF_3', 'COD_LATITUDE', 'COD_LONGITUDE', 'LTR_ATUAL', 'LTR_COLETADA', 'HORA_LEITURA', 'DAT_LEITURA', 'COD_LEITURA_INT', 'STA_ACEITA_LEITURA', 'STA_TROCA', 'EXCECAO', 'VOLUME_ESTIMADO', 'VOLUME_ESTIMADO_ACUM', 'NUM_QUADRA', 'COD_ROTA_LEITURA', 'SUB_CATEGORIA'] # colunas que não quero no dataset
    colunas_normalizar = ['CONS_MEDIDO'] # colunas que quero fazer o min e max, tirando os outliers.
    print(df[['CONS_MEDIDO']])
    colunas_agrupamento = ['DSC_OCORRENCIA']

    # Aqui foi retirado a coluna de sub-categoria para ser feito uma análise mais profunda dos dados presentes nela e como isso pode interferir no modelo
    colunas_padronizar = ['DSC_SIMULTANEA', 'DSC_OCORRENCIA', 'TIPO_LIGACAO', 'CATEGORIA'] #, 'SUB_CATEGORIA' / padronização do texto = regex
    colunas_onehot = ['DSC_SIMULTANEA', 'DSC_OCORRENCIA', 'TIPO_LIGACAO', 'CATEGORIA'] #, 'SUB_CATEGORIA' / para a função de one hot, é melhor usar para texto

    # Nova classe de consumo [alto, medio, baixo]
    coluna_consumo = 'CONS_MEDIDO' # coluna de referencia de consumo

    # Redimensionamento
    coluna_data = 'REFERENCIA' # coluna referencia de datas
    coluna_matricula = 'MATRICULA' # coluna de referencia de id
    colunas_features = ['CONS_MEDIDO'] #,'LTR_ATUAL','LTR_COLETADA'] # aqui para features é onde eu uso as colunas com números, que estão associadas a cada mês

    df_pipe = pipeline_tratamento(df_CONSUMO, colunas_remover, colunas_normalizar, colunas_padronizar, colunas_agrupamento, colunas_onehot, coluna_consumo, coluna_data, coluna_matricula, colunas_features)

    return df_pipe