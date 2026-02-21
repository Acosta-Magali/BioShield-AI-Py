import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import os

def validar_capacidades_bioseguridad():
    print("=== EVALUACIÓN DE CAPACIDAD DE ANTICIPACIÓN DE BROTES ===")
    
    # 1. Cargar datos de prueba y modelo
    df = pd.read_csv("data/processed/datos_con_riesgo.csv")
    modelo = joblib.load("data/models/shield_rf_model.pkl")
    le = joblib.load("data/models/label_encoder.pkl")
    
    # 2. Preparar features (usando la misma lógica que el entrenador)
    from sklearn.preprocessing import LabelEncoder
    df['bio_id_encoded'] = LabelEncoder().fit_transform(df['bio_id'])
    df['patrones_encoded'] = LabelEncoder().fit_transform(df['patrones_identificados'].astype(str))
    
    X = df[['temperatura', 'gc_content', 'bio_id_encoded', 'patrones_encoded']]
    y_true = le.transform(df['nivel_alerta'])
    
    # 3. Realizar predicciones
    y_pred = modelo.predict(X)
    
    # 4. Generar Matriz de Confusión
    cm = confusion_matrix(y_true, y_pred)
    
    # 5. Guardar Reporte en Carpeta de Resultados
    os.makedirs("results", exist_ok=True)
    
    reporte = classification_report(y_true, y_pred, target_names=le.classes_, output_dict=True)
    reporte_df = pd.DataFrame(reporte).transpose()
    reporte_df.to_csv("results/metricas_validacion.csv")
    
    print("\n[MÉTRICAS GENERADAS]")
    print(f"- Precisión Global: {reporte['accuracy']:.4f}")
    print("- Reporte guardado en: 'results/metricas_validacion.csv'")
    
    # 6. Mostrar alerta de seguridad si el Recall para 'CRÍTICO' es bajo
    recall_critico = reporte['CRÍTICO']['recall']
    if recall_critico < 0.95:
        print("\n[⚠️ ALERTA] El sistema tiene fugas detectando brotes críticos.")
    else:
        print("\n[✅ CERTIFICADO] El sistema anticipa brotes con alta confiabilidad.")

if __name__ == "__main__":
    validar_capacidades_bioseguridad()