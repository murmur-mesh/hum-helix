import os
from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
from pydantic import BaseModel
from typing import Optional

import tempfile, shutil

# pydantic hooks really well into fast api
from hum_helix.server.pydantic_types import LoadModelRequest, UnloadModelRequest

app = FastAPI()

app.state.models = {}


# simple ping health check
@app.get("/ping")
def health_check():
    return {"status": "healthy"}


# simple load model and save to state
@app.post("/v1/models/load")
def load_model(req: LoadModelRequest):

    # if its loaded already then return early
    if app.state.models.get(req.model) is not None:
        return {"error": "model already loaded"}

    # otherwise load it and save it to server state
    print("req.download_root:", req.download_root)

    try:
        app.state.models[req.model] = WhisperModel(
            req.model,
            device=req.device,
            compute_type=req.compute_type,
            download_root=req.download_root,
        )
    except Exception as e:
        print("Error loading model:", e)
        return {"error": "failed to load model", "error_message": str(e)}

    return {"model": req.model, "action": "loaded"}


# simple unload model and save to state
@app.post("/v1/models/unload")
def unload_model(req: UnloadModelRequest):
    if app.state.models.get(req.model) is not None:
        del app.state.models[req.model]
        return {"model": req.model, "action": "unloaded"}
    return {"error": "model not loaded"}


# get models loaded
@app.get("/v1/models/loaded")
def list_loaded_models():
    return {"models": list(app.state.models.keys())}


# slow simple transcrbe audio endpoint
@app.post("/v1/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...)):
    print("file.content_type:", file.content_type)
    print("type(file)", type(file))
    ct = file.content_type.strip().lower()

    if ct not in {"audio/wave", "audio/wav", "audio/x-wav"}:
        return {"error": "only wav files are currently supported"}

    # for simplicity we just use the first model loaded
    model_name = next(iter(app.state.models.keys()))
    model = app.state.models[model_name]

    print("model:", model_name)

    print("making temporary file")
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    print("running inference on temporary file:", tmp_path)

    try:
        segments, info = model.transcribe(
            tmp_path, beam_size=1, vad_filter=False, word_timestamps=False
        )
    except Exception as e:
        print("Error during transcription:", e)
        return {"error": "failed to transcribe audio", "error_message": str(e)}
    finally:
        os.remove(tmp_path)

    print("transcribing audio")
    text = ""
    for segment in segments:
        print(f"Segment: {segment.text}")
        text += segment.text

    return {"text": text}


# for starting server with script or directly
def main():
    import uvicorn  # unsure if this should import here or globally

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
