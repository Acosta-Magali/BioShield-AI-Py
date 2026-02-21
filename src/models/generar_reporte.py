import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import confusion_matrix, classification_report
import os

def generar_reporte_visual():
    print("=== GENERANDO REPORTE DE MÉTRICAS DE ANTICIPACIÓN ===")
    
    # 1. Cargar datos y modelo
    df = pd.read_csv("data/processed/datos_con_riesgo.csv")
    modelo = joblib.load("data/models/shield_rf_model.pkl")
    le = joblib.load("data/models/label_encoder.pkl")
    
    # 2. Preparar Features (deben ser las mismas que en el entrenamiento)
    from sklearn.preprocessing import LabelEncoder
    le_id = LabelEncoder()
    le_pat = LabelEncoder()
    
    X = pd.DataFrame({
        'temperatura': df['temperatura'],
        'gc_content': df['gc_content'],
        'bio_id_encoded': le_id.fit_transform(df['bio_id']),
        'patrones_encoded': le_pat.fit_transform(df['patrones_identificados'].astype(str))
    })
    
    y_true = le.transform(df['nivel_alerta'])
    y_pred = modelo.predict(X)

    # 3. Crear Matriz de Confusión
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel('Predicción de la IA')
    plt.ylabel('Riesgo Real (Histórico)')
    plt.title('Matriz de Confusión: Capacidad de Detección de Brotes')
    
    # 4. Guardar resultados
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/matriz_confusion.png")
    print("[OK] Gráfico de Matriz de Confusión guardado en 'results/matriz_confusion.png'")
    
    # 5. Guardar Métricas Detalladas
    reporte = classification_report(y_true, y_pred, target_names=le.classes_)
    with open("results/reporte_final.txt", "w") as f:
        f.write("=== REPORTE DE VALIDACIÓN BIOSHIELD-AI ===\n")
        f.write(reporte)
    print("[OK] Reporte de texto guardado en 'results/reporte_final.txt'")

if __name__ == "__main__":
    generar_reporte_visual()