import os, tempfile, shutil
from fastapi import APIRouter, UploadFile, File, Depends
from hum_helix.server.deps import get_loaded_models

router = APIRouter()


# slow simple transcrbe audio endpoint
@router.post("/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = File(...), loaded_models=Depends(get_loaded_models)
):
    print("file.content_type:", file.content_type)
    print("type(file)", type(file))
    ct = file.content_type.strip().lower()

    if ct not in {"audio/wave", "audio/wav", "audio/x-wav"}:
        return {"error": "only wav files are currently supported"}

    # for simplicity we just use the first model loaded
    model_name = next(iter(loaded_models.keys()))
    model = loaded_models[model_name]

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
