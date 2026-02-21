import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class BioShieldChain:
    def __init__(self):
        # Al iniciar, la cadena solo tiene el bloque semilla
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Bloque Génesis - Inicio del Registro BioShield", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.calculate_hash():
                print(f"⚠️ Error: El hash del bloque {i} ha sido alterado.")
                return False
            
            if current.previous_hash != previous.hash:
                print(f"⚠️ Error: El bloque {i} no apunta correctamente al anterior.")
                return False
        return True

# --- DEMO DE LA CADENA COMPLETA ---
if __name__ == "__main__":
    print("=== REGISTRO BLOCKCHAIN BIOSHIELD-AI ===")
    
    # 1. Inicializar la cadena
    my_bioshield_chain = BioShieldChain()
    
    # 2. Registrar eventos de la IA
    print("\n[INFO] Registrando alertas...")
    my_bioshield_chain.add_block({"alerta": "MODERADA", "sensor": "A1", "valor": 0.55})
    my_bioshield_chain.add_block({"alerta": "CRÍTICA", "sensor": "B2", "valor": 0.89})

    # 3. Mostrar la cadena
    for block in my_bioshield_chain.chain:
        print(f"\nBloque #{block.index}")
        print(f"Hash: {block.hash[:20]}...")
        print(f"Prev: {block.previous_hash[:20]}...")
        print(f"Datos: {block.data}")

    # 4. Validar integridad
    print(f"\n✅ ¿La cadena es íntegra? {my_bioshield_chain.is_chain_valid()}")