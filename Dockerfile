# Usamos una imagen ligera de Python (Linux)
FROM python:3.10-slim

# Variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiamos primero los requerimientos para aprovechar cache
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del codigo
COPY . .

# Comando de arranque (apunta al bot hibrido)
CMD ["python", "src/bot_telegram.py"]