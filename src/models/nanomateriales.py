class Nanomaterial:
    def __init__(self, nombre, composicion, tamaño_nm):
        self.nombre = nombre
        self.composicion = composicion
        self.tamaño_nm = tamaño_nm  # Tamaño en nanómetros
        self.activo = True

    def obtener_info(self):
        return f"Material: {self.nombre} ({self.composicion}) - Tamaño: {self.tamaño_nm}nm"

class NanoSensor(Nanomaterial):
    """Nanomaterial especializado en la detección de patógenos."""
    def __init__(self, nombre, composicion, tamaño_nm, sensibilidad_ppb, objetivo_bio):
        super().__init__(nombre, composicion, tamaño_nm)
        self.sensibilidad_ppb = sensibilidad_ppb  # Partes por billón
        self.objetivo_bio = objetivo_bio  # Ejemplo: 'Proteína Spike', 'ADN Viral'

    def detectar(self, concentracion_actual):
        if concentracion_actual >= self.sensibilidad_ppb:
            return f"✅ [DETECCIÓN] {self.nombre} ha identificado {self.objetivo_bio}."
        return f"⚪ [STANDBY] Concentración por debajo del umbral de {self.sensibilidad_ppb} ppb."

class NanoFiltro(Nanomaterial):
    """Nanomaterial especializado en la limpieza/neutralización."""
    def __init__(self, nombre, composicion, tamaño_nm, eficiencia_filtrado):
        super().__init__(nombre, composicion, tamaño_nm)
        self.eficiencia_filtrado = eficiencia_filtrado  # Porcentaje (0-100)

    def neutralizar(self, volumen_litros):
        reducido = volumen_litros * (self.eficiencia_filtrado / 100)
        return f"🧼 [LIMPIEZA] {self.nombre} ha neutralizado el {self.eficiencia_filtrado}% de carga en {volumen_litros}L."

# --- DEMO DE USO ---
if __name__ == "__main__":
    print("=== REGISTRO DE NANOMATERIALES BIOSHIELD-AI ===")
    
    # 1. Crear un sensor de Grafeno para ADN
    sensor_dna = NanoSensor("Graphene-X1", "Óxido de Grafeno", 1.5, 0.5, "ADN Patógeno")
    print(sensor_dna.obtener_info())
    print(sensor_dna.detectar(0.8))
    
    print("-" * 40)
    
    # 2. Crear un filtro de Nanofibras
    filtro_bio = NanoFiltro("BioNet-Pro", "Nanofibras de Plata", 50, 99.9)
    print(filtro_bio.obtener_info())
    print(filtro_bio.neutralizar(1000))