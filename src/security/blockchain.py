import hashlib
import time
import json

class Block:
    def __init__(self, index, data, previous_hash):
        """
        Representa un bloque individual en la cadena.
        """
        self.index = index
        self.timestamp = time.time()
        self.data = data  # Puede ser un string o un diccionario
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Crea un hash SHA-256 del contenido del bloque.
        """
        # Convertimos el diccionario de datos a string JSON ordenado para evitar inconsistencias
        data_string = json.dumps(self.data, sort_keys=True)
        block_content = f"{self.index}{self.timestamp}{data_string}{self.previous_hash}"
        
        return hashlib.sha256(block_content.encode()).hexdigest()

class BioShieldChain:
    def __init__(self):
        """
        Inicializa la cadena con el bloque génesis.
        """
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Bloque Génesis - Sistema BioShield-AI Iniciado", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        """
        Crea y añade un nuevo bloque a la cadena.
        """
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Recorre la cadena verificando la integridad criptográfica de cada bloque.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Verificar si el hash del bloque actual es correcto
            if current.hash != current.calculate_hash():
                print(f"❌ ERROR: El contenido del Bloque #{i} ha sido manipulado.")
                return False

            # Verificar si el bloque apunta al hash correcto del anterior
            if current.previous_hash != previous.hash:
                print(f"❌ ERROR: El Bloque #{i} tiene un enlace roto con el anterior.")
                return False
                
        return True

# --- SECCIÓN DE PRUEBAS Y AUDITORÍA ---
if __name__ == "__main__":
    print("=== SISTEMA DE SEGURIDAD BLOCKCHAIN BIOSHIELD-AI ===")
    
    # 1. Instanciar la cadena
    bioshield_chain = BioShieldChain()

    # 2. Registrar datos simulados de sensores e IA
    print("\n[INFO] Registrando eventos en el libro mayor inmutable...")
    bioshield_chain.add_block({
        "sensor_id": "SN-001",
        "tipo": "Detección ADN",
        "resultado": "Positivo",
        "riesgo": "ALTO"
    })
    
    bioshield_chain.add_block({
        "sensor_id": "SN-002",
        "tipo": "Simulación Fluido",
        "viento": "5.5 m/s",
        "estado": "Dispersión Activa"
    })

    # 3. Mostrar estado actual
    for b in bioshield_chain.chain:
        print(f"\nBloque #{b.index} | Hash: {b.hash[:20]}...")
        print(f"Datos: {b.data}")

    # 4. Prueba de Integridad (SANA)
    print(f"\n🔍 Verificando integridad inicial: {'✅ VÁLIDA' if bioshield_chain.is_chain_valid() else '❌ CORRUPTA'}")

    # 5. SIMULACIÓN DE ATAQUE (Hackeo de datos)
    print("\n" + "!"*40)
    print("⚠️ SIMULANDO INTENTO DE MANIPULACIÓN ⚠️")
    print("Modificando el riesgo del Bloque #1 de 'ALTO' a 'BAJO'...")
    
    # El atacante intenta cambiar los datos del sensor
    bioshield_chain.chain[1].data["riesgo"] = "BAJO" 
    
    print(f"Datos actuales en Bloque #1: {bioshield_chain.chain[1].data}")
    print("!"*40)

    # 6. Verificación Final tras el ataque
    print(f"\n🔍 Verificando integridad tras el ataque: {'✅ VÁLIDA' if bioshield_chain.is_chain_valid() else '❌ CORRUPTA - ALERTA DE SEGURIDAD'}")