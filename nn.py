from keras.models import Model
from keras.layers import Input, Dense
import pandas as pd

def imputacion(data):

    # Definir el autoencoder
    input_dim = data.shape[1]  # Número de características
    encoding_dim = 5  # Tamaño de la capa de compresión

    # Capa de entrada
    input_layer = Input(shape=(input_dim,))

    # Capa intermedia
    encoded = Dense(encoding_dim, activation='relu')(input_layer)

    # Capa de salida
    decoded = Dense(input_dim, activation='relu')(encoded)

    # Modelo del autoencoder
    autoencoder = Model(input_layer, decoded)

    # Compilar el modelo
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')

    # Datos para entrenar el autoencoder
    # Aquí se usan los datos con valores faltantes
    x_train = data.dropna() # Seleccionar solo filas sin NaN

    # Entrenar el autoencoder
    autoencoder.fit(x_train, x_train, epochs=50, batch_size=32, shuffle=True)
    
    
    df_missing = data.copy()
    df_missing = data.fillna(0)
    
    # Imputar los datos usando el autoencoder
    imputed_data = autoencoder.predict(df_missing)
    
    imputed_data_df = pd.DataFrame(imputed_data, index=data.index, columns=data.columns)

    # Opcional: Reemplazar solo los valores faltantes en los datos originales
    df_imputed = data.copy()
    df_imputed[data.isna()] =imputed_data_df[data.isna()]
    
    return df_imputed