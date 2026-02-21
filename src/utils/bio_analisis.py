from Bio import SeqIO
from Bio.SeqUtils import gc_fraction, molecular_weight

def analizar_secuencia(ruta_archivo, formato="fasta"):
    """
    Lee secuencias y calcula métricas biológicas clave.
    """
    resultados = []
    
    try:
        for registro in SeqIO.parse(ruta_archivo, formato):
            # Calculamos métricas básicas
            porcentaje_gc = gc_fraction(registro.seq) * 100
            peso = molecular_weight(registro.seq)
            
            resultados.append({
                'id': registro.id,
                'gc_content': round(porcentaje_gc, 2),
                'peso_molecular': round(peso, 2),
                'secuencia_limpia': str(registro.seq).upper()
            })
            
        print(f"[EXITO] Analizadas {len(resultados)} secuencias en formato {formato}.")
        return resultados
    except Exception as e:
        print(f"[ERROR] No se pudo procesar el archivo biológico: {e}")
        return []