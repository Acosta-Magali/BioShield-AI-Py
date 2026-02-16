import pandas as pd

def integrar_fuentes(df_ambiental, lista_secuencias):
    """
    Une los datos ambientales con los biológicos en un esquema único.
    """
    if df_ambiental is None or not lista_secuencias:
        return None

    # 1. Convertimos la lista de Biopython a un DataFrame de Pandas
    datos_bio = []
    for seq in lista_secuencias:
        datos_bio.append({
            'bio_id': seq.id,
            'secuencia_dna': str(seq.seq),
            'longitud_pb': len(seq.seq)
        })
    df_bio = pd.DataFrame(datos_bio)

    # 2. Unión (Merge/Join)
    # Como es un prototipo, haremos un cross-join o asignación por proximidad
    # En BioShield-AI, asumimos que las secuencias pertenecen al área de los sensores
    df_ambiental['key'] = 1
    df_bio['key'] = 1
    
    df_integrado = pd.merge(df_ambiental, df_bio, on='key').drop("key", axis=1)
    
    print(f"[EXITO] Esquema integrado generado. Dimensiones: {df_integrado.shape}")
    return df_integrado