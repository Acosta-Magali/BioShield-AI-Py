#!/bin/bash
echo "🛡️ Iniciando despliegue de BioShield-AI..."
docker build -t bioshield-ai .
echo "🚀 Lanzando contenedor en puerto 8501..."
docker run -p 8501:8501 bioshield-ai