from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from TTS.api import TTS
import os
import torch

app = FastAPI()

# Cargar el modelo Coqui XTTS v2 al iniciar
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Cargando modelo en dispositivo: {device}")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

@app.post("/generar-voz")
async def generar_voz(texto: str = Form(...)):
    output_path = "output.wav"
    speaker_wav = "locutor.wav.mp3"

    if not os.path.exists(speaker_wav):
        raise HTTPException(status_code=400, detail="No se encontró el archivo de voz base (locutor.wav.mp3)")

    try:
        tts.tts_to_file(
            text=texto,
            speaker_wav=speaker_wav,
            language="es",
            file_path=output_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el audio: {str(e)}")

    return FileResponse(output_path, media_type="audio/wav", filename="anuncio.wav")
