import pandas as pd
import random
from datetime import datetime, timedelta

def generar_datos_ambientales_mock(n=100):
    """Genera n registros de sensores ambientales con variaciones aleatorias."""
    datos = []
    inicio = datetime.now()
    
    for i in range(n):
        fecha = inicio - timedelta(hours=i)
        datos.append({
            'fecha': fecha.strftime("%Y-%m-%d %H:%M:%S"),
            'sensor_id': f"SENS-{random.randint(100, 999)}",
            'temperatura': round(random.uniform(15.0, 42.0), 1),
            'humedad': round(random.uniform(30.0, 90.0), 1),
            'pm25': round(random.uniform(0.0, 150.0), 1)
        })
    
    return pd.DataFrame(datos)

def generar_secuencia_adn_mock(longitud=30):
    """Genera una cadena de ADN aleatoria."""
    return "".join(random.choice("ATGC") for _ in range(longitud))

def guardar_mock_data(df_amb, num_secuencias=10):
    """Guarda los archivos mock en la carpeta raw para pruebas."""
    # Guardar CSV
    df_amb.to_csv("data/raw/mock_ambiental.csv", index=False)
    
    # Guardar FASTA
    with open("data/raw/mock_biologico.fasta", "w") as f:
        for i in range(num_secuencias):
            seq = generar_secuencia_adn_mock(random.randint(25, 50))
            f.write(f">seq_mock_{i}|Virus_Simulado\n{seq}\n")
    
    print(f"[MOCK] Generados {len(df_amb)} registros ambientales y {num_secuencias} secuencias.")