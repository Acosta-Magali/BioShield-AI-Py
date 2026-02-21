from utils.generador_mock import generar_datos_ambientales_mock, guardar_mock_data
from utils.cargador_datos import cargar_csv_ambiental, cargar_fasta_biologico
from utils.limpiador_datos import limpiar_datos_ambientales
from utils.bio_analisis import analizar_secuencia_avanzado
from utils.integrador import integrar_fuentes
import time

def ejecutar_stress_test(volumen=500):
    print(f"=== INICIANDO PRUEBA DE ESTRÉS: {volumen} REGISTROS ===")
    start_time = time.time()

    # 1. Generar datos ficticios masivos
    df_mock = generar_datos_ambientales_mock(volumen)
    guardar_mock_data(df_mock, num_secuencias=20)

    # 2. Correr el Pipeline con los datos mock
    print("\n[PROCESANDO] Pipeline en marcha...")
    
    # Carga y Limpieza
    df_clean = limpiar_datos_ambientales(cargar_csv_ambiental("data/raw/mock_ambiental.csv"))
    
    # Bio-Análisis
    analisis_bio = analizar_secuencia_avanzado("data/raw/mock_biologico.fasta")
    
    # Integración
    secuencias = cargar_fasta_biologico("data/raw/mock_biologico.fasta")
    df_final = integrar_fuentes(df_clean, secuencias)

    end_time = time.time()
    duracion = round(end_time - start_time, 2)

    print("\n=== RESULTADOS DE LA PRUEBA DE ESTRÉS ===")
    print(f"Registros procesados: {len(df_final)}")
    print(f"Tiempo total: {duracion} segundos")
    print(f"Rendimiento: {round(len(df_final)/duracion, 2)} registros/seg")
    
    if len(df_final) > 0:
        print("[OK] El sistema soportó la carga de datos masiva.")

if __name__ == "__main__":
    ejecutar_stress_test(500)