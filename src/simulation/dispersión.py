import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

def simulador_dispersion():
    print("=== SIMULADOR DE DISPERSIÓN DE CONTAMINANTES (BioShield-AI) ===")

    # Configuración del espacio (1D)
    L = 100.0    # Longitud del canal/área (metros)
    nx = 100     # Número de puntos en la rejilla
    dx = L / (nx - 1)
    x = np.linspace(0, L, nx)

    # Parámetros físicos
    D = 0.5      # Coeficiente de Difusión
    v = 1.0      # Velocidad del fluido (Advección)
    t_max = 50   # Tiempo total de simulación
    nt = 100     # Pasos de tiempo
    t = np.linspace(0, t_max, nt)

    # Condición inicial: Un "pico" de contaminante en el centro (x=20)
    C0 = np.exp(-0.5 * ((x - 20)/2)**2) 

    def ecuacion_difusion_adveccion(C, t, x, v, D, dx):
        dCdt = np.zeros_like(C)
        
        for i in range(1, nx - 1):
            # Término de Advección (Diferencia centrada)
            adveccion = -v * (C[i+1] - C[i-1]) / (2 * dx)
            # Término de Difusión (Segunda derivada)
            difusion = D * (C[i+1] - 2*C[i] + C[i-1]) / (dx**2)
            
            dCdt[i] = adveccion + difusion
            
        return dCdt

    # Resolver la ecuación diferencial
    print("[PROCESANDO] Resolviendo EDO con SciPy...")
    solucion = odeint(ecuacion_difusion_adveccion, C0, t, args=(x, v, D, dx))

    # Visualización
    plt.figure(figsize=(10, 6))
    for i in range(0, nt, 20):
        plt.plot(x, solucion[i], label=f't = {t[i]:.1f}s')

    plt.title("Simulación de Dispersión de Contaminantes en Fluidos")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Concentración del Patógeno")
    plt.legend()
    plt.grid(True)
    
    # Guardar resultado
    os.makedirs("results/simulations", exist_ok=True)
    plt.savefig("results/simulations/dispersion_fluidos.png")
    print("[OK] Simulación completada. Gráfico guardado en 'results/simulations/dispersion_fluidos.png'")
    plt.show()

if __name__ == "__main__":
    simulador_dispersion()