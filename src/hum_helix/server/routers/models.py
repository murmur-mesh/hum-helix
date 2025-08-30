from fastapi import APIRouter, Depends
from hum_helix.server.pydantic_types import LoadModelRequest, UnloadModelRequest
from hum_helix.server.deps import get_loaded_models
from faster_whisper import WhisperModel

# routes defined:
# /v1/models/load
# /v1/models/unload
# /v1/models/loaded

router = APIRouter()


# simple load model and save to state
@router.post("/models/load")
def load_model(req: LoadModelRequest, loaded_models=Depends(get_loaded_models)):

    # if its loaded already then return early
    if loaded_models.get(req.model) is not None:
        return {"error": "model already loaded"}

    # otherwise load it and save it to server state
    print("req.download_root:", req.download_root)

    try:
        loaded_models[req.model] = WhisperModel(
            req.model,
            device=req.device,
            compute_type=req.compute_type,
            download_root=req.download_root,
        )
    except Exception as e:
        print("Error loading model:", e)
        return {"error": f"failed to load model {req.model}", "error_message": str(e)}

    return {"model": req.model, "action": "loaded"}


# simple unload model and save to state
@router.post("/models/unload")
def unload_model(req: UnloadModelRequest, loaded_models=Depends(get_loaded_models)):
    if loaded_models.get(req.model) is not None:
        del loaded_models[req.model]
        return {"model": req.model, "action": "unloaded"}
    return {"error": f"model not loaded: {req.model}"}


# get models loaded
@router.get("/models/loaded")
def list_loaded_models(loaded_models=Depends(get_loaded_models)):
    return {"models": list(loaded_models.keys())}
