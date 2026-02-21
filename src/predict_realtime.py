import pandas as pd
import numpy as np
import joblib
import os

# Configuración de rutas
MODEL_PATH_RF = "data/models/shield_rf_model.pkl"
LABEL_ENCODER_PATH = "data/models/label_encoder.pkl"

def predecir_riesgo_biologico(temperatura, gc_content, tiene_patrones=False):
    """
    Función optimizada para predicción sin warnings.
    """
    # 1. Cargar modelos
    rf_model = joblib.load(MODEL_PATH_RF)
    le_alerta = joblib.load(LABEL_ENCODER_PATH)
    
    # 2. Crear DataFrame con nombres de columnas (Evita el UserWarning)
    patrones_val = 1 if tiene_patrones else 0
    input_df = pd.DataFrame([[temperatura, gc_content, 0, patrones_val]], 
                            columns=['temperatura', 'gc_content', 'bio_id_encoded', 'patrones_encoded'])
    
    # 3. Predicción
    pred_class_idx = rf_model.predict(input_df)[0]
    pred_label = le_alerta.inverse_transform([pred_class_idx])[0]
    
    # 4. Probabilidad
    probs = rf_model.predict_proba(input_df)[0]
    prob_max = np.max(probs) * 100

    return {
        "nivel_alerta": pred_label,
        "confianza": f"{prob_max:.2f}%"
    }

# ==========================================================
# BLOQUE INTERACTIVO (VA AL FINAL)
# ==========================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("      SISTEMA DE MONITOREO BIOSHIELD-AI V1.0")
    print("="*50)
    
    try:
        t = float(input("Ingrese Temperatura Ambiente (°C): "))
        gc = float(input("Ingrese Contenido GC del Patógeno (0.0 - 1.0): "))
        p = input("¿Se detectaron patrones de virulencia? (s/n): ").lower() == 's'
        
        res = predecir_riesgo_biologico(t, gc, p)
        
        print("\n" + "-"*30)
        print(f"ESTADO DEL SISTEMA: {res['nivel_alerta']}")
        print(f"CONFIANZA DE LA IA: {res['confianza']}")
        print("-"*30)
        
        if res['nivel_alerta'] in ['ALTO', 'CRÍTICO']:
            print("🚨 ACCIÓN RECOMENDADA: ACTIVAR PROTOCOLO DE CONTENCIÓN")
        else:
            print("✅ ESTADO: Vigilancia de rutina")
            
    except ValueError:
        print("Error: Por favor ingrese valores numéricos válidos.")