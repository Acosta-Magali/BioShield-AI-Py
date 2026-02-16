from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales
from utils.integrador import integrar_fuentes 

def ejecutar_pipeline_ingesta():
    print("=== INICIANDO PIPELINE DE INGESTA Y ESQUEMA INTEGRADO ===")

    # 1. Rutas
    ruta_csv = "data/raw/datos_ambientales.csv"
    ruta_fasta = "data/raw/secuencias_virus.fasta"

    # 2. Procesamiento Individual
    print("\n[PASO 1] Procesando Datos Ambientales...")
    df_raw = cargar_csv_ambiental(ruta_csv)
    df_clean = limpiar_datos_ambientales(df_raw)

    print("\n[PASO 2] Procesando Datos Biológicos...")
    secuencias = cargar_fasta_biologico(ruta_fasta)

    # 3. Integración bajo el nuevo Schema
    print("\n[PASO 3] Integrando fuentes bajo el nuevo esquema...")
    df_final = integrar_fuentes(df_clean, secuencias)
    
    if df_final is not None:
        print("\n--- VISTA PREVIA DEL ESQUEMA INTEGRADO ---")
        # Mostramos las columnas clave que definen tu nuevo Schema
        columnas_schema = ['fecha', 'sensor_id', 'temperatura', 'bio_id', 'longitud_pb']
        print(df_final[columnas_schema].head())
        
        # Guardar el resultado para el futuro entrenamiento de IA
        df_final.to_csv("data/processed/datos_integrados.csv", index=False)
        print("\n[OK] Archivo 'data/processed/datos_integrados.csv' guardado.")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()