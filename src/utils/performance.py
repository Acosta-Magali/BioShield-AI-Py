import time
import psutil
import os

def profile_resources(func):
    """Decorador para medir tiempo, CPU y Memoria de una función."""
    def wrapper(*args, **kwargs):
        # Medición inicial
        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss / (1024 * 1024)  # MB
        start_time = time.time()
        
        # Ejecución de la función
        result = func(*args, **kwargs)
        
        # Medición final
        end_time = time.time()
        end_mem = process.memory_info().rss / (1024 * 1024)  # MB
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        print(f"\n--- 📊 Reporte de Rendimiento: {func.__name__} ---")
        print(f"⏱️ Tiempo de ejecución: {end_time - start_time:.4f} seg")
        print(f"🧠 Consumo de Memoria: {end_mem - start_mem:.4f} MB (Total: {end_mem:.2f} MB)")
        print(f"⚡ Uso de CPU: {cpu_usage}%")
        print("-------------------------------------------\n")
        
        return result
    return wrapper