from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from TTS.api import TTS
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo XTTS-v2 optimizado para CPU
device = "cpu"
print("Cargando modelo Coqui XTTS...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

@app.post("/generar-voz")
async def generar_voz(texto: str = Form(...)):
    output_path = "output.wav"
    speaker_wav = "locutor.wav.mp3"  # Tu archivo de voz de referencia en el repositorio

    if not os.path.exists(speaker_wav):
        raise HTTPException(status_code=500, detail="No se encontró el archivo de voz de referencia (locutor.wav.mp3)")

    try:
        # Generar clonación de voz usando tu archivo
        tts.tts_to_file(
            text=texto,
            speaker_wav=speaker_wav,
            language="es",
            file_path=output_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el audio con Coqui: {str(e)}")

    return FileResponse(output_path, media_type="audio/wav", filename="anuncio_voz.wav")

@app.get("/")
def home():
    return {"mensaje": "API de Coqui TTS con clonación de voz activa"}
