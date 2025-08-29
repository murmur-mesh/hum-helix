from fastapi import FastAPI
from faster_whisper import WhisperModel
from pydantic import BaseModel
from typing import Optional

# use constr and conint for regex constraits in the future


# pydantic hooks amazing into fast api
class LoadModelRequest(BaseModel):
    model: str
    device: str
    compute_type: str
    download_root: Optional[str] = None


class UnloadModelRequest(BaseModel):
    model: str


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


# simple get models loaded
@app.get("/v1/models/loaded")
def list_loaded_models():
    return {"models": list(app.state.models.keys())}


# for starting server with script or directly
def main():
    import uvicorn  # unsure if this should import here or globally

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
