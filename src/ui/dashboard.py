import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime

# Configuración de rutas para importar módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.security.blockchain import BioShieldChain

# Inicialización de la Blockchain en el estado de la sesión de Streamlit
# Esto evita que la cadena se reinicie cada vez que movemos un slider
if 'bioshield_chain' not in st.session_state:
    st.session_state.bioshield_chain = BioShieldChain()

def main():
    st.set_page_config(page_title="BioShield-AI Control", layout="wide")
    
    st.title("🛡️ Sistema de Integración BioShield-AI")
    
    # --- BARRA LATERAL: ENTRADA DE MODELOS IA ---
    st.sidebar.header("🕹️ Simulación de Sensores (IA)")
    sensor_id = st.sidebar.selectbox("Seleccionar Sensor", ["SN-001", "SN-002", "SN-003"])
    riesgo_input = st.sidebar.select_slider("Nivel de Riesgo Detectado", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])
    temp = st.sidebar.number_input("Temperatura Ambiente (°C)", value=25.0)
    
    if st.sidebar.button("Registrar Evento en Blockchain"):
        nuevo_evento = {
            "sensor_id": sensor_id,
            "riesgo": riesgo_input,
            "temp": temp,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.bioshield_chain.add_block(nuevo_evento)
        st.sidebar.success("Evento anclado a la red.")

    # --- COLUMNAS DE VISUALIZACIÓN ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Historial de Riesgo (Modelos)")
        # Extraemos datos de la Blockchain para el gráfico
        chain_data = []
        for block in st.session_state.bioshield_chain.chain:
            if isinstance(block.data, dict):
                chain_data.append(block.data)
        
        if chain_data:
            df = pd.DataFrame(chain_data)
            fig = px.line(df, x="timestamp", y="temp", color="sensor_id", 
                         title="Evolución de Temperatura por Sensor", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos suficientes para graficar.")

    with col2:
        st.subheader("🛡️ Verificador de Integridad")
        es_valida = st.session_state.bioshield_chain.auditar_cadena()
        if es_valida:
            st.success("CADENA ÍNTEGRA: Los datos coinciden con el registro SHA-256.")
        else:
            st.error("ALERTA: Se ha detectado una discrepancia en la base de datos.")

    # --- TABLA DE LA BASE DE DATOS BLOCKCHAIN ---
    st.markdown("---")
    st.subheader("🔗 Libro Mayor de Eventos (Trazabilidad)")
    
    # Transformamos la cadena en un DataFrame para mostrarlo bonito
    display_data = []
    for b in st.session_state.bioshield_chain.chain:
        display_data.append({
            "Bloque": b.index,
            "Hash": b.hash[:15] + "...",
            "Datos": str(b.data),
            "Previo": b.previous_hash[:15] + "..."
        })
    
    st.dataframe(pd.DataFrame(display_data), use_container_width=True)

if __name__ == "__main__":
    main()