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
    """Escribe los resultados en un archivo físico."""
    with open(REPORT_PATH, "a", encoding="utf-8") as f:
        f.write(metrica + "\n")

def profile_resources(func):
    """Mide el impacto en hardware y genera reporte persistente."""
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
        
        # Solo imprimimos y guardamos si no es una función interna muy repetitiva
        guardar_reporte(reporte)
        return result
    return wrapper

# --- CLASES DE BLOCKCHAIN ---

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = json.dumps(self.data, sort_keys=True)
        block_content = f"{self.index}{self.timestamp}{data_string}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

class BioShieldChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "GENESIS", "0")

    def get_latest_block(self):
        """MÉTODO RECUPERADO: Necesario para el Dashboard."""
        return self.chain[-1]

    @profile_resources
    def add_block(self, data):
        new_block = Block(len(self.chain), data, self.get_latest_block().hash)
        self.chain.append(new_block)
        return new_block

    @profile_resources
    def auditar_cadena(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash() or current.previous_hash != previous.hash:
                return False
        return True

    @profile_resources
    def buscar_por_sensor(self, sensor_id):
        return [b for b in self.chain if isinstance(b.data, dict) and b.data.get("sensor_id") == sensor_id]