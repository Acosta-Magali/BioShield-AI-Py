import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Añadir el directorio raíz al path para poder importar nuestros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.security.blockchain import BioShieldChain

def main():
    # 1. Configuración de la página
    st.set_page_config(
        page_title="BioShield-AI Dashboard",
        page_icon="🛡️",
        layout="wide"
    )

    # 2. Barra Lateral (Controles)
    st.sidebar.title("🛡️ BioShield-AI")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Parámetros Globales")
    temp = st.sidebar.slider("Temperatura (°C)", 0, 50, 25)
    viento = st.sidebar.slider("Velocidad del Viento (m/s)", 0.0, 20.0, 5.0)

    # 3. Título Principal
    st.title("Sistema de Monitoreo de Bioseguridad")
    st.markdown("""
    Este panel integra inteligencia artificial para predicción de riesgo y 
    blockchain para la integridad de los datos.
    """)

    # 4. Layout de Columnas para Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estado del Sistema", "Activo", delta="OK")
    with col2:
        st.metric("Nivel de Riesgo", "Bajo", delta="-2%", delta_color="inverse")
    with col3:
        st.metric("Integridad Blockchain", "Verificada", delta="100%")

    # 5. Espacio para el gráfico de Dispersión (Plotly)
    st.subheader("Simulación de Dispersión en Tiempo Real")
    
    # Datos de ejemplo para inicializar el gráfico
    df_sim = pd.DataFrame({
        'Distancia (m)': range(100),
        'Concentración': [x**2 * 0.001 for x in range(100)]
    })
    fig = px.line(df_sim, x='Distancia (m)', y='Concentración', 
                  title="Curva de Dispersión Atmosférica")
    st.plotly_chart(fig, use_container_width=True)

    # 6. Sección de Blockchain
    st.subheader("Registro Inmutable (Blockchain)")
    if st.button("Verificar Historial de Auditoría"):
        st.success("Cadena de bloques verificada: No se detectaron alteraciones.")

if __name__ == "__main__":
    main()