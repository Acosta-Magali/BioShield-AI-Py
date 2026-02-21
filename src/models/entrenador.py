import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def entrenar_modelo_historico():
    print("=== ENTRENAMIENTO CON DATASET HISTÓRICO ===")
    
    # 1. Cargar datos (Asegúrate de haber corrido el stress test o tener datos procesados)
    ruta_datos = "data/processed/datos_con_riesgo.csv"
    if not os.path.exists(ruta_datos):
        print("[ERROR] No se encuentra el dataset procesado. Corré primero el pipeline de ingesta.")
        return

    df = pd.read_csv(ruta_datos)
    print(f"[INFO] Dataset cargado: {len(df)} registros.")

    # 2. Preprocesamiento (Encoding)
    le_id = LabelEncoder()
    le_patrones = LabelEncoder()
    le_alerta = LabelEncoder()

    df['bio_id_encoded'] = le_id.fit_transform(df['bio_id'])
    df['patrones_encoded'] = le_patrones.fit_transform(df['patrones_identificados'].astype(str))
    
    X = df[['temperatura', 'gc_content', 'bio_id_encoded', 'patrones_encoded']]
    y = le_alerta.fit_transform(df['nivel_alerta'])

    # 3. División de datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Entrenamiento
    print("[PROCESANDO] Entrenando Random Forest con datos históricos...")
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    # 5. Evaluación de Precisión
    y_pred = modelo_rf.predict(X_test)
    precision = accuracy_score(y_test, y_pred)
    
    print("\n=== RESULTADOS DEL ENTRENAMIENTO ===")
    print(f"Precisión del Modelo: {precision * 100:.2f}%")
    print("\nReporte Detallado:")
    # Mapeamos los nombres originales de las alertas para el reporte
    print(classification_report(y_test, y_pred, target_names=le_alerta.classes_))

    # 6. Guardar Modelo y Encoders
    os.makedirs("data/models", exist_ok=True)
    joblib.dump(modelo_rf, "data/models/shield_rf_model.pkl")
    joblib.dump(le_alerta, "data/models/label_encoder.pkl")
    print("\n[OK] Modelo histórico guardado exitosamente.")

if __name__ == "__main__":
    entrenar_modelo_historico()