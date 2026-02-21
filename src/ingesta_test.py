import pandas as pd
from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales
from utils.integrador import integrar_fuentes 
from utils.bio_analisis import analizar_secuencia_avanzado

def ejecutar_pipeline_ingesta():
    print("=== INICIANDO PIPELINE DE DETECCIÓN DE PATRONES ===")

    # 1. Rutas
    ruta_csv = "data/raw/datos_ambientales.csv"
    ruta_fasta = "data/raw/secuencias_virus.fasta"

    # [PASO 1] Datos Ambientales
    print("\n[PASO 1] Procesando Datos Ambientales...")
    df_raw = cargar_csv_ambiental(ruta_csv)
    df_clean = limpiar_datos_ambientales(df_raw)

    # [PASO 2] Bio-Análisis y Identificación de Patrones
    print("\n[PASO 2] Analizando ADN e Identificando Patrones...")
    analisis_bio = analizar_secuencia_avanzado(ruta_fasta)
    
    # Mostramos los hallazgos en consola
    if analisis_bio:
        for a in analisis_bio:
            print(f"ID: {a['id']} | Patrones: {a['patrones_detectados']} | GC: {a['gc_content']}%")

    # [PASO 3] Integración y Generación de Dataset para IA
    print("\n[PASO 3] Integrando hallazgos al esquema maestro...")
    # Necesitamos el objeto 'secuencias' original para el integrador
    secuencias_originales = cargar_fasta_biologico(ruta_fasta)
    df_final = integrar_fuentes(df_clean, secuencias_originales)

    if df_final is not None:
        # Agregamos la columna de patrones al DataFrame final para que la IA la vea
        # Mapeamos los resultados del análisis al DataFrame
        dict_patrones = {res['id']: res['patrones_detectados'] for res in analisis_bio}
        df_final['patrones_identificados'] = df_final['bio_id'].map(dict_patrones)

        print("\n--- VISTA PREVIA DEL SISTEMA DE DETECCIÓN ---")
        columnas_vista = ['fecha', 'temperatura', 'bio_id', 'patrones_identificados']
        print(df_final[columnas_vista].head())
        
        # Guardamos el dataset enriquecido
        df_final.to_csv("data/processed/datos_integrados.csv", index=False)
        print(f"\n[OK] Dataset enriquecido guardado con {len(df_final)} registros.")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()