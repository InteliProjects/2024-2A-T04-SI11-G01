import pandas as pd
import pickle

def model_predict(treated_df):
    # Carregar o modelo
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)

    # Realizar as predições
    predictions = model.predict(treated_df)

    # Adicionar as predições ao DataFrame original
    treated_df['Predictions'] = predictions

    # Retornar o DataFrame atualizado
    return treated_df