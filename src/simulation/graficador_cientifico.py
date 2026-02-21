import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

def generar_grafico_evolucion():
    print("=== GENERADOR DE GRÁFICOS CIENTÍFICOS BIOSHIELD-AI ===")

    # 1. Configuración de la simulación (idéntica a la anterior para coherencia)
    L, nx = 100.0, 100
    x = np.linspace(0, L, nx)
    D, v = 0.5, 1.0
    t = np.linspace(0, 50, 100)
    dx = L / (nx - 1)
    C0 = np.exp(-0.5 * ((x - 20)/2)**2)

    def ecuacion(C, t, x, v, D, dx):
        dCdt = np.zeros_like(C)
        for i in range(1, nx - 1):
            adveccion = -v * (C[i+1] - C[i-1]) / (2 * dx)
            difusion = D * (C[i+1] - 2*C[i] + C[i-1]) / (dx**2)
            dCdt[i] = adveccion + difusion
        return dCdt

    solucion = odeint(ecuacion, C0, t, args=(x, v, D, dx))

    # 2. Creación del gráfico científico
    plt.style.use('seaborn-v0_8-muted') # Estilo limpio y profesional
    fig, ax = plt.subplots(figsize=(12, 7))

    # Usamos un mapa de colores (Viridis) para representar el tiempo
    colors = plt.cm.viridis(np.linspace(0, 1, 10))
    pasos_a_graficar = np.linspace(0, len(t)-1, 10, dtype=int)

    for idx, i in enumerate(pasos_a_graficar):
        ax.plot(x, solucion[i], color=colors[idx], lw=2, 
                label=f't = {t[i]:.1f}s')

    # 3. Estética Científica (Anotaciones y Formato)
    ax.set_title("Evolución Espacio-Temporal de la Pluma de Contaminante", fontsize=14, fontweight='bold')
    ax.set_xlabel("Distancia desde el punto de origen (m)", fontsize=12)
    ax.set_ylabel("Concentración Relativa ($C/C_0$)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Añadir flecha de dirección del flujo
    ax.annotate('Dirección del Flujo (Viento/Agua)', xy=(60, 0.1), xytext=(40, 0.1),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2))

    ax.legend(title="Evolución Temporal", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # 4. Guardado en alta resolución
    os.makedirs("results/simulations", exist_ok=True)
    ruta_img = "results/simulations/evolucion_temporal_cientifica.png"
    plt.savefig(ruta_img, dpi=300) # 300 DPI para calidad de impresión
    
    print(f"[OK] Gráfico científico generado con éxito en: {ruta_img}")
    plt.show()

if __name__ == "__main__":
    generar_grafico_evolucion()