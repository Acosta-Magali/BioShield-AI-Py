import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

def preparar_datos_y_entrenar():
    print("=== INICIANDO FASE DE INTELIGENCIA ARTIFICIAL ===")
    
    # 1. Cargar el dataset que generamos con el cruce de datos
    df = pd.read_csv("data/processed/datos_con_riesgo.csv")
    
    # 2. Preprocesamiento (Encoding)
    # Convertimos categorías de texto a números para la IA
    le_id = LabelEncoder()
    le_patrones = LabelEncoder()
    le_alerta = LabelEncoder()

    df['bio_id_encoded'] = le_id.fit_transform(df['bio_id'])
    df['patrones_encoded'] = le_patrones.fit_transform(df['patrones_identificados'].astype(str))
    
    # Nuestra "Y" (lo que queremos predecir) es el nivel de alerta
    y = le_alerta.fit_transform(df['nivel_alerta'])
    
    # Nuestras "X" (características)
    X = df[['temperatura', 'gc_content', 'bio_id_encoded', 'patrones_encoded']]

    # 3. Dividir datos (80% entrenamiento, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Definición de Algoritmos
    print("\n[MODELO 1] Entrenando Random Forest para Clasificación...")
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    print("[MODELO 2] Entrenando Regresión Logística para Tendencias...")
    modelo_lr = LogisticRegression(max_iter=1000)
    modelo_lr.fit(X_train, y_train)

    # 5. Guardar modelos para uso futuro
    joblib.dump(modelo_rf, "data/models/shield_rf_model.pkl")
    joblib.dump(le_alerta, "data/models/label_encoder.pkl")
    
    print("\n[EXITO] Algoritmos definidos y modelos guardados en 'data/models/'")
    return X_test, y_test, modelo_rf

if __name__ == "__main__":
    # Asegúrate de crear la carpeta data/models antes de correrlo
    import os
    os.makedirs("data/models", exist_ok=True)
    preparar_datos_y_entrenar()