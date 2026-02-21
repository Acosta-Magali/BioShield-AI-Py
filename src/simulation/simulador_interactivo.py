import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

def correr_simulacion_personalizada():
    print("\n" + "="*50)
    print("   CONFIGURACIÓN DE SIMULACIÓN DE DISPERSIÓN")
    print("="*50)

    try:
        # 1. Entrada de parámetros por el usuario
        v = float(input("Velocidad del fluido/viento (m/s) [Ej: 0.5 - 5.0]: "))
        D = float(input("Coeficiente de difusión (m²/s) [Ej: 0.1 - 2.0]: "))
        cantidad = float(input("Cantidad de contaminante inicial (Escala 0.1 - 5.0): "))
        posicion_inicial = float(input("Punto de liberación (metros entre 0 y 50): "))

        # 2. Configuración técnica
        L, nx = 100.0, 100
        x = np.linspace(0, L, nx)
        t = np.linspace(0, 50, 100)
        dx = L / (nx - 1)
        
        # Condición inicial basada en la entrada del usuario
        C0 = cantidad * np.exp(-0.5 * ((x - posicion_inicial)/2)**2)

        # 3. Función del modelo (Advección-Difusión)
        def modelo_fisico(C, t, x, v, D, dx):
            dCdt = np.zeros_like(C)
            for i in range(1, nx - 1):
                adveccion = -v * (C[i+1] - C[i-1]) / (2 * dx)
                difusion = D * (C[i+1] - 2*C[i] + C[i-1]) / (dx**2)
                dCdt[i] = adveccion + difusion
            return dCdt

        # 4. Resolución
        print(f"\n[PROCESANDO] Simulando a {v} m/s...")
        solucion = odeint(modelo_fisico, C0, t, args=(x, v, D, dx))

        # 5. Visualización del escenario personalizado
        plt.figure(figsize=(10, 6))
        plt.plot(x, C0, 'r--', label="Punto de Liberación")
        plt.plot(x, solucion[-1], 'b-', label=f"Estado Final (t=50s)")
        
        plt.fill_between(x, solucion[-1], color='blue', alpha=0.2)
        plt.title(f"Escenario: V={v}m/s, D={D}, Masa={cantidad}")
        plt.xlabel("Distancia (m)")
        plt.ylabel("Concentración")
        plt.legend()
        plt.grid(True)

        # Guardar el escenario específico
        os.makedirs("results/simulations", exist_ok=True)
        plt.savefig("results/simulations/escenario_personalizado.png")
        print("\n✅ Simulación finalizada. Imagen guardada como 'escenario_personalizado.png'")
        plt.show()

    except ValueError:
        print("❌ Error: Por favor ingrese solo valores numéricos.")

if __name__ == "__main__":
    correr_simulacion_personalizada()