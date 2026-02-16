import pandas as pd
import numpy as np

def limpiar_datos_ambientales(df):
    if df is None:
        return None
        
    df_clean = df.copy()

    # 1. Normalizar Fechas: Forzar formato datetime único (Ajustado)
    print("   -> Normalizando fechas...")
    df_clean['fecha'] = pd.to_datetime(df_clean['fecha'], dayfirst=True, errors='coerce', format='mixed')

    # 2. Manejar Valores Nulos en PM2.5
    if 'nivel_contaminacion_pm25' in df_clean.columns:
        print("   -> Rellenando valores nulos...")
        media_pm25 = df_clean['nivel_contaminacion_pm25'].mean()
        df_clean['nivel_contaminacion_pm25'] = df_clean['nivel_contaminacion_pm25'].fillna(media_pm25)

    # 3. Estandarizar Unidades (Fahrenheit a Celsius)
    if 'temperatura' in df_clean.columns:
        print("   -> Verificando unidades de temperatura...")
        # Si la temperatura es > 45, asumimos que es Fahrenheit y convertimos
        df_clean['temperatura'] = df_clean['temperatura'].apply(
            lambda x: round((x - 32) * 5/9, 1) if x > 45 else x
        )

    # 4. Eliminar Duplicados
    print(f"   -> Eliminando duplicados (Filas antes: {len(df_clean)})")
    df_clean = df_clean.drop_duplicates()
    print(f"   -> Filas después: {len(df_clean)}")

    return df_clean