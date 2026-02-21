from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales
from utils.integrador import integrar_fuentes 
from utils.bio_analisis import analizar_secuencia # Importación limpia al inicio

def ejecutar_pipeline_ingesta():
    print("=== INICIANDO PIPELINE DE INGESTA Y ESQUEMA INTEGRADO ===")

    # 1. Rutas de archivos
    ruta_csv = "data/raw/datos_ambientales.csv"
    ruta_fasta = "data/raw/secuencias_virus.fasta"

    # [PASO 1] Procesamiento de Datos Ambientales
    print("\n[PASO 1] Procesando Datos Ambientales (Pandas)...")
    df_raw = cargar_csv_ambiental(ruta_csv)
    df_clean = limpiar_datos_ambientales(df_raw) # Aquí definimos df_clean

    # [PASO 2] Configurando y ejecutando herramientas Biopython
    print("\n[PASO 2] Ejecutando análisis bioinformático (Biopython)...")
    
    # Obtenemos las métricas avanzadas (GC%, Peso)
    metricas_bio = analizar_secuencia(ruta_fasta)
    
    # Cargamos el objeto original de secuencias para el integrador
    secuencias = cargar_fasta_biologico(ruta_fasta) # Aquí definimos secuencias
    
    if metricas_bio:
        for m in metricas_bio:
            print(f"ID: {m['id']} | GC%: {m['gc_content']}% | Peso: {m['peso_molecular']} Da")
    
    # [PASO 3] Integración bajo el nuevo Schema
    print("\n[PASO 3] Integrando fuentes bajo el nuevo esquema...")
    
    # Ahora que df_clean y secuencias existen, el integrador no fallará
    df_final = integrar_fuentes(df_clean, secuencias)
    
    if df_final is not None:
        print("\n--- VISTA PREVIA DEL ESQUEMA INTEGRADO ---")
        # Columnas clave para verificar tu nuevo Schema
        columnas_schema = ['fecha', 'sensor_id', 'temperatura', 'bio_id', 'longitud_pb']
        print(df_final[columnas_schema].head())
        
        # Guardar el resultado procesado
        df_final.to_csv("data/processed/datos_integrados.csv", index=False)
        print("\n[OK] Archivo 'data/processed/datos_integrados.csv' guardado.")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()