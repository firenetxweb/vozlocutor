FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema esenciales
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Actualizar pip e instalar paquetes de uno en uno para ahorrar RAM
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch==2.1.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir fastapi uvicorn python-multipart
RUN pip install --no-cache-dir TTS

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
