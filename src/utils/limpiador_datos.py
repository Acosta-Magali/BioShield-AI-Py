import pandas as pd
import pandas as pd

def limpiar_datos_ambientales(df):
    """
    Limpia los datos: convierte fechas y rellena vacíos.
    """
    df_limpio = df.copy()

    # Convertir fecha si existe
    if 'fecha' in df_limpio.columns:
        df_limpio['fecha'] = pd.to_datetime(df_limpio['fecha'])
    
    # Rellenar niveles de contaminación vacíos con el promedio
    if 'nivel_contaminacion_pm25' in df_limpio.columns:
        promedio = df_limpio['nivel_contaminacion_pm25'].mean()
        df_limpio['nivel_contaminacion_pm25'] = df_limpio['nivel_contaminacion_pm25'].fillna(promedio)
        
    return df_limpio