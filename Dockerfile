FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 1. Instalar PyTorch primero de manera ligera
RUN pip install --no-cache-dir torch==2.1.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu

# 2. Instalar dependencias del servidor web
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# 3. Instalar Coqui TTS al final
RUN pip install --no-cache-dir TTS

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
