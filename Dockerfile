# 1. Imagen base
FROM python:3.11-slim

# 2. Variables de entorno (Formato actualizado para evitar warnings)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalar Pip y Streamlit explícitamente primero
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir streamlit pandas plotly psutil

# 6. Copiar el resto del proyecto e instalar otros requerimientos si existen
COPY . .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# 7. Crear carpeta de datos
RUN mkdir -p data

# 8. Puerto
EXPOSE 8501

# 9. Comando de ejecución
ENTRYPOINT ["streamlit", "run", "src/ui/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]