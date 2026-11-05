import io
import os
import tempfile
import torchaudio as ta
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import Response
from contextlib import asynccontextmanager
from chatterbox.tts_turbo import ChatterboxTurboTTS

# Global variable to hold the model
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model once on startup
    print("Loading model into memory...")
    ml_models["tts"] = ChatterboxTurboTTS.from_pretrained(device="cuda")
    print("Model loaded successfully!")
    yield
    # Clean up on shutdown
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/generate")
async def generate_audio(
    text: str = Form(...), 
    ref_audio: UploadFile = File(None)
):
    model = ml_models["tts"]
    
    # Use uploaded reference audio or fall back to a local default
    if ref_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await ref_audio.read())
            ref_path = tmp.name
    else:
        ref_path = "ref.wav"

    try:
        # Generate the audio
        wav = model.generate(text, audio_prompt_path=ref_path)

        # Save the tensor to an in-memory bytes buffer
        buffer = io.BytesIO()
        ta.save(buffer, wav, model.sr, format="wav")
        buffer.seek(0)
        
        # Return the audio file directly in the HTTP response
        return Response(content=buffer.read(), media_type="audio/wav")
    
    finally:
        # Clean up the temporary file if one was created
        if ref_audio and os.path.exists(ref_path):
            os.remove(ref_path)

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
