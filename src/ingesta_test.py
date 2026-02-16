from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales

def ejecutar_pipeline_ingesta():
    print("=== INICIANDO PIPELINE DE INGESTA DE DATOS (VERSION FINAL) ===")

    # 1. Rutas de archivos 
    ruta_csv = "data/raw/datos_ambientales.csv"
    ruta_fasta = "data/raw/secuencias_virus.fasta"

    # 2. Procesar Datos Ambientales (Usando Pandas) 
    print("\n[PASO 1] Procesando Datos Ambientales...")
    df_raw = cargar_csv_ambiental(ruta_csv)
    
    if df_raw is not None:
        print("Datos crudos cargados con éxito.")
        # Limpiamos los datos usando la lógica de limpiador_datos.py
        df_clean = limpiar_datos_ambientales(df_raw)
        print("Datos limpios (promedios calculados y fechas convertidas):")
        print(df_clean.tail(2))

    # 3. Procesar Datos Biológicos (Usando Biopython) [cite: 12]
    print("\n[PASO 2] Procesando Datos Biológicos...")
    secuencias = cargar_fasta_biologico(ruta_fasta)
    
    if secuencias:
        for seq in secuencias:
            print(f"ID: {seq.id} | Longitud: {len(seq.seq)} pb")

if __name__ == "__main__":
    ejecutar_pipeline_ingesta()