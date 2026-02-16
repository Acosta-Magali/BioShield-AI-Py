import pandas as pd
from Bio import SeqIO
import os

def cargar_csv_ambiental(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] No se encontró: {ruta_archivo}")
        return None
    
    try:
        df = pd.read_csv(ruta_archivo)
        print(f"[EXITO] CSV cargado. Filas: {len(df)}")
        return df
    except Exception as e:
        print(f"[ERROR] CSV: {e}")
        return None

def cargar_fasta_biologico(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] No se encontró: {ruta_archivo}")
        return []

    try:
        secuencias = list(SeqIO.parse(ruta_archivo, "fasta"))
        print(f"[EXITO] FASTA cargado. Secuencias: {len(secuencias)}")
        return secuencias
    except Exception as e:
        print(f"[ERROR] FASTA: {e}")
        return []