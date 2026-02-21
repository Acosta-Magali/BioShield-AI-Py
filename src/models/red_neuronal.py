import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def entrenar_red_neuronal():
    print("=== CONFIGURANDO RED NEURONAL: BIOSHIELD-AI ===")

    # 1. Carga de datos
    df = pd.read_csv("data/processed/datos_con_riesgo.csv")
    
    # 2. Preprocesamiento específico para Deep Learning
    le_id = LabelEncoder()
    le_patrones = LabelEncoder()
    le_alerta = LabelEncoder()

    X = np.column_stack([
        df['temperatura'],
        df['gc_content'],
        le_id.fit_transform(df['bio_id']),
        le_patrones.fit_transform(df['patrones_identificados'].astype(str))
    ])
    
    y = le_alerta.fit_transform(df['nivel_alerta'])
    # Convertimos y a "One-Hot Encoding" (necesario para redes neuronales multiclase)
    y_cat = tf.keras.utils.to_categorical(y)

    # Escalado de datos (Vital para Redes Neuronales)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_cat, test_size=0.2, random_state=42)

    # 3. Arquitectura de la Red Neuronal
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)), # Capa entrada
        Dropout(0.2),                                                # Evita sobreajuste
        Dense(32, activation='relu'),                                # Capa oculta
        Dense(y_cat.shape[1], activation='softmax')                   # Capa salida (probabilidades)
    ])

    # 4. Compilación
    model.compile(optimizer='adam', 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])

    # 5. Entrenamiento
    print("\n[PROCESANDO] Entrenando Red Neuronal por 20 épocas...")
    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1, verbose=1)

    # 6. Evaluación
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n=== RESULTADOS DE LA RED NEURONAL ===")
    print(f"Precisión Final (Test): {accuracy * 100:.2f}%")

    # 7. Guardar modelo y scaler
    os.makedirs("data/models", exist_ok=True)
    model.save("data/models/shield_nn_model.h5")
    joblib.dump(scaler, "data/models/scaler_nn.pkl")
    joblib.dump(le_alerta, "data/models/label_encoder_nn.pkl")
    
    print("\n[OK] Red Neuronal guardada en 'data/models/shield_nn_model.h5'")

if __name__ == "__main__":
    entrenar_red_neuronal()