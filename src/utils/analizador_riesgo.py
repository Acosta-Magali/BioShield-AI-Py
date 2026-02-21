import pandas as pd  # <--- ESTA ES LA LÍNEA QUE FALTABA

def evaluar_riesgo(fila):
    """
    Cruza biomarcadores ambientales con hallazgos biológicos.
    Retorna un score de 0 a 100 y una categoría.
    """
    score = 0
    temp = fila['temperatura']
    gc = fila['gc_content']
    patrones = fila.get('patrones_identificados', "Ninguno")
    
    # REGLA 1: Correlación Temp/Estabilidad (GC%)
    # Un GC alto indica que el virus resiste mejor el calor.
    if temp > 30 and gc > 50:
        score += 40
    elif temp > 25:
        score += 20

    # REGLA 2: Presencia de Patrones Críticos
    if "MOTIVO_ALPHA" in patrones:
        score += 50
    elif "VIRULENCIA" in patrones:
        score += 30
    
    # Clasificación
    if score >= 80:
        return score, "CRÍTICO"
    if score >= 50:
        return score, "ALTO"
    if score >= 20:
        return score, "MODERADO"
    
    return score, "BAJO"

def aplicar_analisis_cruzado(df_integrado):
    """Aplica la evaluación de riesgo a todo el dataset."""
    resultados = df_integrado.apply(evaluar_riesgo, axis=1)
    df_integrado[['riesgo_score', 'nivel_alerta']] = pd.DataFrame(resultados.tolist(), index=df_integrado.index)
    return df_integrado