import pandas as pd
import Bio
from Bio.Seq import Seq

def probar_entorno():
    print("--- Verificando entorno de BioShield AI-Py ---")
    
    # 1. Prueba de Pandas (Datos)
    try:
        df = pd.DataFrame({'Biosensor': ['A1', 'B2'], 'Lectura': [0.5, 0.8]})
        print(f"[OK] Pandas versión {pd.__version__} funcionando.")
        print("   Ejemplo de datos:")
        print(df)
    except ImportError:
        print("[ERROR] Pandas no está instalado.")

    # 2. Prueba de Biopython (Biología)
    try:
        print(f"[OK] Biopython versión {Bio.__version__} funcionando.")
        # Crear una secuencia de ADN simple
        adn = Seq("ATGCGT")
        print(f"   Secuencia de prueba: {adn}")
        print(f"   Traducción a proteína: {adn.translate()}")
    except ImportError:
        print("[ERROR] Biopython no está instalado.")

if __name__ == "__main__":
    probar_entorno()