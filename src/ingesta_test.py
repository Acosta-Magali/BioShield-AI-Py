import pandas as pd
from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales
from utils.integrador import integrar_fuentes 
from utils.bio_analisis import analizar_secuencia_avanzado
from utils.analizador_riesgo import aplicar_analisis_cruzado

def ejecutar_pipeline_ingesta():
    print("=== SISTEMA BIOSHIELD-AI: PIPELINE DE INTEGRACIÓN Y RIESGO ===")

    # 1. Definición de rutas
    ruta_csv = "data/raw/datos_ambientales.csv"
    ruta_fasta = "data/raw/secuencias_virus.fasta"

    # [PASO 1] Procesamiento de Datos Ambientales (Pandas)
    print("\n[PASO 1] Procesando Datos Ambientales...")
    df_raw = cargar_csv_ambiental(ruta_csv)
    df_clean = limpiar_datos_ambientales(df_raw)

    # [PASO 2] Bio-Análisis y Identificación de Patrones (Biopython + Regex)
    print("\n[PASO 2] Analizando ADN e Identificando Patrones...")
    analisis_bio = analizar_secuencia_avanzado(ruta_fasta)
    
    if analisis_bio:
        print(f"   -> {len(analisis_bio)} secuencias analizadas.")
        for a in analisis_bio:
            print(f"      - ID: {a['id']} | Patrones: {a['patrones_detectados']} | GC: {a['gc_content']}%")

    # [PASO 3] Integración y Cruce de Datos (Correlación)
    print("\n[PASO 3] Integrando fuentes y cruzando biomarcadores...")
    secuencias_originales = cargar_fasta_biologico(ruta_fasta)
    df_final = integrar_fuentes(df_clean, secuencias_originales)

    if df_final is not None:
        dict_patrones = {res['id']: res['patrones_detectados'] for res in analisis_bio}
        dict_gc = {res['id']: res['gc_content'] for res in analisis_bio}
        
        df_final['patrones_identificados'] = df_final['bio_id'].map(dict_patrones)
        df_final['gc_content'] = df_final['bio_id'].map(dict_gc)

        # APLICAMOS LA LÓGICA DE CRUCE (Evaluación de Riesgo)
        df_final = aplicar_analisis_cruzado(df_final)

        print("\n--- VISTA PREVIA DEL SISTEMA DE ALERTA TEMPRANA ---")
        columnas_finales = [
            'fecha', 'temperatura', 'bio_id', 'gc_content', 
            'patrones_identificados', 'riesgo_score', 'nivel_alerta'
        ]
        print(df_final[columnas_finales].head())
        
        ruta_salida = "data/processed/datos_con_riesgo.csv"
        df_final.to_csv(ruta_salida, index=False)
        print(f"\n[OK] Pipeline finalizado. Dataset de riesgo guardado en: {ruta_salida}")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()