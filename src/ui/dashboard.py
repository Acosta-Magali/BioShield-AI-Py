import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def main():
    st.set_page_config(page_title="BioShield-AI | Tactical Dashboard", layout="wide")
    
    # --- HEADER ---
    st.title("🛡️ BioShield-AI: Centro de Control de Bioseguridad")
    st.info("Monitoreo en tiempo real con respaldo de integridad en Blockchain.")

    # --- DATOS SIMULADOS (Para visualización) ---
    # Evolución temporal
    time_index = pd.date_range(start=datetime.now(), periods=24, freq='H')
    temp_data = np.random.normal(25, 2, size=24)
    risk_score = np.cumsum(np.random.randn(24) * 0.1) + 1
    
    df_temporal = pd.DataFrame({'Hora': time_index, 'Riesgo': risk_score, 'Temp': temp_data})

    # Mapa de Calor (Coordenadas simuladas)
    df_heat = pd.DataFrame({
        'lat': np.random.uniform(-34.1, -34.2, 15),
        'lon': np.random.uniform(-59.0, -59.1, 15),
        'intensidad': np.random.uniform(0.1, 1.0, 15)
    })

    # --- VISTA PRINCIPAL (Layout) ---
    
    # Fila 1: Métricas Críticas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Índice de Riesgo", f"{risk_score[-1]:.2f}", "+5%")
    m2.metric("Sensores Activos", "12/12", "100%")
    m3.metric("Último Hash", "9a6ca41...", delta="Válido", delta_color="normal")
    m4.metric("Alertas 24h", "3", "-1", delta_color="inverse")

    st.markdown("---")

    # Fila 2: Gráficas Principales
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("📈 Evolución Temporal del Riesgo")
        fig_evol = px.area(df_temporal, x='Hora', y='Riesgo', 
                          color_discrete_sequence=['#ff4b4b'])
        fig_evol.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
        st.plotly_chart(fig_evol, use_container_width=True)

    with col_der:
        st.subheader("📍 Mapa de Calor de Amenazas")
        # Usamos un gráfico de dispersión sobre mapa (puedes usar st.map para algo simple)
        st.map(df_heat) 

    st.markdown("---")

    # Fila 3: Panel de Alertas y Blockchain
    st.subheader("🚨 Panel de Alertas Recientes")
    
    alertas_data = [
        {"Hora": "21:45", "Evento": "Detección SN-001", "Riesgo": "ALTO", "Estado": "🛡️ En Blockchain"},
        {"Hora": "20:30", "Evento": "Variación Térmica", "Riesgo": "BAJO", "Estado": "🛡️ En Blockchain"},
        {"Hora": "18:15", "Evento": "Falla de Comunicación", "Riesgo": "MODERADO", "Estado": "🛡️ En Blockchain"},
    ]
    st.table(pd.DataFrame(alertas_data))

if __name__ == "__main__":
    main()