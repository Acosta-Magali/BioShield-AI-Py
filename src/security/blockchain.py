import hashlib
import time
import json

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
        return Block(0, "SYSTEM_START: Inicio de registros BioShield-AI", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)
        print(f"📦 Bloque #{new_block.index} añadido con éxito.")

    def auditar_cadena(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                print(f"🛑 ALERTA: Datos alterados en Bloque #{i}")
                return False
            if current.previous_hash != previous.hash:
                print(f"🛑 ALERTA: Enlace roto en Bloque #{i}")
                return False
        print("🔍 Auditoría completada: No se detectaron anomalías.")
        return True

    def buscar_por_sensor(self, sensor_id):
        """Rastrea todos los bloques relacionados con un sensor específico."""
        print(f"\n🔍 [TRAZABILIDAD] Buscando historial para el sensor: {sensor_id}")
        hallazgos = [bloque for bloque in self.chain if isinstance(bloque.data, dict) and bloque.data.get("sensor_id") == sensor_id]
        if not hallazgos:
            print(f"⚠️ No se encontraron registros para el sensor {sensor_id}.")
        return hallazgos

    def buscar_por_riesgo(self, nivel):
        """Filtra el historial por nivel de riesgo."""
        print(f"\n🔍 [AUDITORÍA] Filtrando incidentes con riesgo: {nivel}")
        return [bloque for bloque in self.chain if isinstance(bloque.data, dict) and bloque.data.get("riesgo") == nivel]

# --- PRUEBA DE TRAZABILIDAD Y AUDITORÍA ---
if __name__ == "__main__":
    print("=== SISTEMA DE SEGURIDAD Y TRAZABILIDAD BIOSHIELD-AI ===")
    
    # 1. Creamos la base de datos
    bioshield_db = BioShieldChain()

    # 2. Registramos datos históricos para probar la búsqueda
    print("\n[SISTEMA] Poblando registros históricos...")
    bioshield_db.add_block({"sensor_id": "SN-001", "riesgo": "ALTO", "patogeno": "Virus-X"})
    bioshield_db.add_block({"sensor_id": "SN-002", "riesgo": "BAJO", "patogeno": "None"})
    bioshield_db.add_block({"sensor_id": "SN-001", "riesgo": "MODERADO", "patogeno": "Virus-X (Residuo)"})

    # 3. Ejecutar búsqueda de trazabilidad (Muestra que podemos rastrear el origen)
    historial_sn001 = bioshield_db.buscar_por_sensor("SN-001")
    for b in historial_sn001:
        print(f"-> Bloque #{b.index} | Riesgo: {b.data['riesgo']} | Patógeno: {b.data['patogeno']}")

    # 4. Filtrar por riesgo crítico
    alertas_criticas = bioshield_db.buscar_por_riesgo("ALTO")
    print(f"Total de alertas críticas encontradas: {len(alertas_criticas)}")

    # 5. SIMULACIÓN DE AUDITORÍA Y ATAQUE
    print("\n--- Iniciando Auditoría de Rutina ---")
    bioshield_db.auditar_cadena()

    print("\n--- [SIMULACIÓN DE ATAQUE] Alterando datos del Bloque 1 ---")
    bioshield_db.chain[1].data["riesgo"] = "BAJO"  # Manipulación maliciosa
    
    print("--- Re-iniciando Auditoría Post-Incidente ---")
    if not bioshield_db.auditar_cadena():
        print("🚨 RESULTADO: Integridad comprometida. Trazabilidad no confiable.")