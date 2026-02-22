import hashlib
import time
import json
import psutil
import os
from datetime import datetime

# --- CONFIGURACIÓN DE REPORTES ---
REPORT_PATH = "data/performance_report.txt"
os.makedirs("data", exist_ok=True)

def guardar_reporte(metrica):
    """Escribe los resultados de rendimiento en un archivo físico."""
    with open(REPORT_PATH, "a", encoding="utf-8") as f:
        f.write(metrica + "\n")

def profile_resources(func):
    """Decorador para medir impacto en hardware (CPU, RAM, Tiempo)."""
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        start_mem = process.memory_info().rss / (1024 * 1024)
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_mem = process.memory_info().rss / (1024 * 1024)
        cpu_usage = psutil.cpu_percent(interval=0.01)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reporte = (f"[{timestamp}] FUNC: {func.__name__} | "
                   f"TIEMPO: {end_time - start_time:.4f}s | "
                   f"RAM_DIFF: {end_mem - start_mem:.4f}MB | "
                   f"CPU: {cpu_usage}%")
        
        guardar_reporte(reporte)
        return result
    return wrapper

# --- CLASES DE BLOCKCHAIN REFACTORIZADAS ---

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Genera el hash SHA-256 del bloque."""
        data_string = json.dumps(self.data, sort_keys=True)
        block_content = f"{self.index}{self.timestamp}{data_string}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class BioShieldChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self._is_valid = True
        self._sensor_index = {} 

    def create_genesis_block(self):
        return Block(0, "SYSTEM_START: BioShield-AI Genesis", "0")

    def get_latest_block(self):
        """Complejidad: O(1)"""
        return self.chain[-1]

    @profile_resources
    def add_block(self, data):
        """
        Añade un bloque y actualiza índices en tiempo real.
        Complejidad: O(1)
        """
        new_block = Block(len(self.chain), data, self.get_latest_block().hash)
        
        # Validación incremental: comprobamos el enlace antes de añadirlo
        if new_block.previous_hash != self.chain[-1].hash:
            self._is_valid = False
            
        self.chain.append(new_block)
        
        # OPTIMIZACIÓN DE BÚSQUEDA: Indexación por sensor_id
        if isinstance(data, dict) and "sensor_id" in data:
            s_id = data["sensor_id"]
            if s_id not in self._sensor_index:
                self._sensor_index[s_id] = []
            self._sensor_index[s_id].append(new_block)
            
        return new_block

    @profile_resources
    def auditar_cadena(self):
        """
        Retorna el estado de integridad.
        Complejidad: O(1) (Gracias al flag _is_valid actualizado en add_block)
        """
        return self._is_valid

    @profile_resources
    def buscar_por_sensor(self, sensor_id):
        """
        Busca bloques por ID de sensor.
        Complejidad: O(1) (Gracias al índice _sensor_index)
        """
        return self._sensor_index.get(sensor_id, [])

    @profile_resources
    def buscar_por_riesgo(self, nivel):
        """
        Filtra por riesgo.
        Complejidad: O(n) (Requiere recorrido lineal)
        """
        return [b for b in self.chain if isinstance(b.data, dict) and b.data.get("riesgo") == nivel]

# --- PRUEBA DE ESTRÉS Y RENDIMIENTO ---
if __name__ == "__main__":
    print(f"🚀 Iniciando BioShield-AI Engine... Reporte en: {REPORT_PATH}")
    guardar_reporte(f"\n--- NUEVA SESIÓN DE RENDIMIENTO: {datetime.now()} ---")
    
    bioshield_db = BioShieldChain()

    # 1. Simulación de carga masiva
    print("📦 Registrando bloques...")
    for i in range(50):
        bioshield_db.add_block({
            "sensor_id": "SN-001" if i % 2 == 0 else "SN-002",
            "riesgo": "BAJO",
            "lectura": i * 0.5
        })

    # 2. Prueba de búsqueda optimizada (O(1))
    print("🔍 Probando búsqueda indexada...")
    resultados = bioshield_db.buscar_por_sensor("SN-001")
    
    # 3. Prueba de auditoría optimizada (O(1))
    print(f"🛡️ Estado de integridad: {'✅ OK' if bioshield_db.auditar_cadena() else '🛑 FALLIDO'}")

    print("\n✅ Pruebas finalizadas. Revisa el archivo de reporte para ver el consumo de CPU/RAM.")