# 🛡️ BioShield-AI: Biosecurity & Traceability Engine

**BioShield-AI** es una plataforma integral de monitoreo ambiental que combina simulación física, inteligencia artificial y tecnología Blockchain para garantizar la integridad de los datos en escenarios de riesgo biológico.

## 🚀 Guía de Instalación

Sigue estos pasos para configurar el entorno de desarrollo en tu máquina local:

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/BioShield-AI.git](https://github.com/tu-usuario/BioShield-AI.git)
cd BioShield-AI
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run src/ui/dashboard.py
```

## 🛠️ Documentación de la API Interna

### BioShieldChain (Módulo de Seguridad)

Clase principal encargada de la inmutabilidad de los datos.

- add_block(data): 
     - Descripción: Valida y añade un nuevo registro a la cadena.
     - Complejidad: $O(1)$ (Optimizado con indexación).
     
- auditar_cadena():
     - Descripción: Verifica la integridad de los hashes SHA-256.
     - Complejidad: $O(1)$ (Uso de caché de estado).
     
- buscar_por_sensor(sensor_id): 
     - Descripción: Recupera el historial completo de un sensor específico.
     - Complejidad: $O(1)$.
     
     
### Performance Profiler (Módulo de Sostenibilidad)

Decoradores para el monitoreo de "Ingeniería Verde".

- @profile_resources:
     - Uso: Colocar sobre cualquier función para registrar consumo de CPU, RAM y tiempo en data/performance_report.txt.
     
### 🌿 Ingeniería Verde (Green Computing)

Este proyecto aplica principios de Software Sostenible:

- Eficiencia Algorítmica: Reducción de carga computacional mediante optimización de complejidad Big O.

- Monitoreo Energético: Generación automática de reportes de consumo en vatios-hora (Wh).

## 📂 Estructura del Proyecto

BioShield-AI/
├── data/               # Reportes de performance y persistencia
├── src/
│   ├── security/       # Lógica de Blockchain (SHA-256)
│   ├── ui/             # Dashboard interactivo (Streamlit)
│   ├── utils/          # Herramientas de análisis y Green Metrics
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación principal

## 📦 Paso Técnico: Generar `requirements.txt`

Para que el punto 3 de la guía de instalación funcione, debes generar el archivo de dependencias. Ejecuta este comando en tu terminal:

```powershell
pip freeze > requirements.txt
```

## 📚 Hito Finalizado: Documentación y Guía de Instalación

Se ha completado la capa de comunicación técnica del proyecto, facilitando su escalabilidad y despliegue por otros desarrolladores.

### Logros:

- Guía de Instalación: Paso a paso detallado para configuración de entornos virtuales y dependencias.

- Documentación de API: Especificación técnica de métodos clave y su complejidad computacional ($O$-notation).

- Manual de Arquitectura: Descripción de la estructura de carpetas y flujo de datos.

- Transparencia Verde: Sección dedicada a explicar el bajo impacto energético del software.