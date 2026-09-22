from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from gtts import gTTS
import os

app = FastAPI()

@app.post("/generar-voz")
async def generar_voz(texto: str = Form(...)):
    output_path = "output.mp3"

    try:
        # Generar audio con voz natural en español
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el audio: {str(e)}")

    return FileResponse(output_path, media_type="audio/mpeg", filename="anuncio.mp3")

@app.get("/")
def home():
    return {"mensaje": "API de voz activa y funcionando correctamente"}
