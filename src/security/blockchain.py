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
        # Convertimos a JSON ordenado para que el hash sea siempre igual ante los mismos datos
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
        """Verifica la integridad criptográfica total."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Prueba 1: ¿Los datos coinciden con el hash?
            if current.hash != current.calculate_hash():
                print(f"🛑 ALERTA: Datos alterados en Bloque #{i}")
                return False

            # Prueba 2: ¿El enlace con el bloque anterior es correcto?
            if current.previous_hash != previous.hash:
                print(f"🛑 ALERTA: Enlace roto en Bloque #{i}")
                return False

        print("🔍 Auditoría completada: No se detectaron anomalías.")
        return True

# --- PRUEBA DE AUDITORÍA ---
if __name__ == "__main__":
    print("=== SISTEMA DE SEGURIDAD BLOCKCHAIN BIOSHIELD-AI ===")
    
    # 1. Creamos la base de datos
    bioshield_db = BioShieldChain()
    
    # 2. Registramos datos legítimos
    bioshield_db.add_block({"alerta": "BAJA", "virus": "None"})
    bioshield_db.add_block({"alerta": "CRÍTICA", "virus": "SARS-CoV-2-Delta"})

    # 3. Primera Auditoría (Debe salir OK)
    print("\n--- Iniciando Auditoría de Rutina ---")
    bioshield_db.auditar_cadena()

    # 4. SIMULACIÓN DE ATAQUE
    print("\n--- [SIMULACIÓN DE ATAQUE] Alterando datos del Bloque 1 ---")
    # Cambiamos los datos manualmente sin recalcular el hash
    bioshield_db.chain[1].data = {"alerta": "BAJA", "virus": "None (Falsificado)"}
    print(f"Datos manipulados: {bioshield_db.chain[1].data}")

    # 5. Segunda Auditoría (Debe detectar el error)
    print("\n--- Re-iniciando Auditoría Post-Incidente ---")
    if not bioshield_db.auditar_cadena():
        print("🚨 RESULTADO: Integridad comprometida. Bloqueando acceso a datos.")
    else:
        print("✅ Resultado: Cadena íntegra.")
    