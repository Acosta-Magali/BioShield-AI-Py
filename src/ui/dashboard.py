import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime

# Configuración de rutas para importar módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.security.blockchain import BioShieldChain

# --- INICIALIZACIÓN DE ESTADO ---
if 'bioshield_chain' not in st.session_state:
    st.session_state.bioshield_chain = BioShieldChain()

def obtener_color_riesgo(nivel):
    """Asigna colores, iconos y mensajes según el umbral de riesgo."""
    config = {
        "BAJO": {"color": "#28a745", "icono": "🟢", "mensaje": "SITUACIÓN NORMAL"},
        "MODERADO": {"color": "#ffc107", "icono": "🟡", "mensaje": "PRECAUCIÓN - MONITOREO ACTIVADO"},
        "ALTO": {"color": "#fd7e14", "icono": "🟠", "mensaje": "ALERTA - POSIBLE AMENAZA"},
        "CRÍTICO": {"color": "#dc3545", "icono": "🔴", "mensaje": "EMERGENCIA - ACCIÓN INMEDIATA"}
    }
    return config.get(nivel, {"color": "#6c757d", "icono": "⚪", "mensaje": "SIN DATOS"})

def main():
    # 1. Configuración de la página
    st.set_page_config(
        page_title="BioShield-AI Tactical Dashboard",
        page_icon="🛡️",
        layout="wide"
    )

    # 2. Lógica de Datos Actuales (Último bloque de la cadena)
    ultimo_bloque = st.session_state.bioshield_chain.get_latest_block()
    nivel_actual = "BAJO"
    if isinstance(ultimo_bloque.data, dict):
        nivel_actual = ultimo_bloque.data.get("riesgo", "BAJO")
    
    status = obtener_color_riesgo(nivel_actual)

    # 3. SEMÁFORO VISUAL (Banner Superior)
    st.markdown(f"""
        <div style="
            background-color: {status['color']};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 26px;
            margin-bottom: 25px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        ">
            {status['icono']} ESTADO DE BIOSEGURIDAD: {nivel_actual} <br>
            <span style="font-size: 16px; font-weight: normal;">{status['mensaje']}</span>
        </div>
    """, unsafe_allow_html=True)

    # 4. BARRA LATERAL (Entrada de Datos e IA)
    st.sidebar.title("🛡️ Panel de Control")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕹️ Simulación de Sensores")
    
    id_sensor = st.sidebar.selectbox("Sensor ID", ["SN-001", "SN-002", "SN-003", "Mobile-Unit-A"])
    riesgo_sim = st.sidebar.select_slider("Nivel de Riesgo (IA)", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])
    temp_sim = st.sidebar.slider("Temperatura (°C)", 0.0, 50.0, 25.0)
    
    if st.sidebar.button("Registrar Evento en Blockchain"):
        nuevo_registro = {
            "sensor_id": id_sensor,
            "riesgo": riesgo_sim,
            "temp": temp_sim,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.bioshield_chain.add_block(nuevo_registro)
        st.sidebar.success("Bloque añadido y verificado.")
        st.rerun() # Recarga para actualizar el semáforo inmediatamente

    # 5. LAYOUT DE COLUMNAS (Gráficos e Integridad)
    col_graf, col_audit = st.columns([2, 1])

    with col_graf:
        st.subheader("📈 Historial de Parámetros Críticos")
        
        # Procesar datos de la cadena para graficar
        datos_grafico = []
        for b in st.session_state.bioshield_chain.chain:
            if isinstance(b.data, dict):
                datos_grafico.append(b.data)
        
        if len(datos_grafico) > 0:
            df = pd.DataFrame(datos_grafico)
            fig = px.line(df, x="timestamp", y="temp", color="sensor_id", 
                         markers=True, line_shape="spline", title="Evolución Térmica por Sensor")
            fig.update_layout(template="plotly_dark" if nivel_actual != "BAJO" else "plotly")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Esperando registros para generar visualización...")

    with col_audit:
        st.subheader("🛡️ Auditoría Forense")
        valida = st.session_state.bioshield_chain.auditar_cadena()
        if valida:
            st.success("INTEGRIDAD: OK (Verificación SHA-256)")
        else:
            st.error("INTEGRIDAD: COMPROMETIDA")
        
        st.metric("Total Bloques", len(st.session_state.bioshield_chain.chain))
        st.metric("Último Hash", ultimo_bloque.hash[:12] + "...")

    # 6. TABLA DE TRAZABILIDAD (Blockchain)
    st.markdown("---")
    st.subheader("🔗 Libro Mayor de Eventos (Blockchain Explorer)")
    
    trazabilidad = []
    for b in st.session_state.bioshield_chain.chain:
        trazabilidad.append({
            "Índice": b.index,
            "Sello de Tiempo": datetime.fromtimestamp(b.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "Datos": str(b.data),
            "Hash Actual": b.hash[:20] + "...",
            "Hash Previo": b.previous_hash[:20] + "..."
        })
    
    st.dataframe(pd.DataFrame(trazabilidad), use_container_width=True)

if __name__ == "__main__":
    main()