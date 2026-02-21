import re
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction, molecular_weight

def buscar_patrones(secuencia, patrones_dict):
    """
    Busca patrones específicos (motivos) en una secuencia de ADN.
    Retorna un string con los hallazgos.
    """
    hallazgos = []
    for nombre, patron in patrones_dict.items():
        # Buscamos el patrón (incluyendo solapamientos)
        coincidencias = [m.start() for m in re.finditer(f"(?=({patron}))", secuencia)]
        if coincidencias:
            hallazgos.append(f"{nombre}(x{len(coincidencias)})")
    
    return ", ".join(hallazgos) if hallazgos else "Ninguno detectado"

def analizar_secuencia_avanzado(ruta_archivo, formato="fasta"):
    """
    Lee secuencias, calcula métricas y detecta patrones de patógenos.
    """
    # Diccionario de firmas sospechosas (puedes agregar más aquí)
    # Ejemplo: GATC suele asociarse a sitios de metilación en bacterias
    firmas_peligro = {
        'VIRULENCIA_POTENCIAL': 'GATC',
        'ESTABILIDAD_ALTA': 'CCGG',
        'MOTIVO_ALPHA': 'ATGC'
    }
    
    resultados = []
    
    try:
        for registro in SeqIO.parse(ruta_archivo, formato):
            seq_str = str(registro.seq).upper()
            
            # Calculamos métricas
            porcentaje_gc = round(gc_fraction(registro.seq) * 100, 2)
            peso = round(molecular_weight(registro.seq), 2)
            
            # Buscamos patrones
            patrones = buscar_patrones(seq_str, firmas_peligro)
            
            resultados.append({
                'id': registro.id,
                'gc_content': porcentaje_gc,
                'peso_molecular': peso,
                'patrones_detectados': patrones,
                'secuencia': seq_str
            })
            
        print(f"[EXITO] Análisis avanzado completado para {len(resultados)} secuencias.")
        return resultados
    except Exception as e:
        print(f"[ERROR] Error en el análisis bioinformático: {e}")
        return []