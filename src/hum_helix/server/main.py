from fastapi import FastAPI
from faster_whisper import WhisperModel

app = FastAPI()

app.state.models = {}


# simple ping health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# simple load model and save to state
@app.post("/v1/models/{id}:load")
def load_model(id: str):
    if app.state.models.get(id) is None:
        app.state.models[id] = WhisperModel(
            "small.en", device="cpu", compute_type="int8"
        )
        if app.state.models.get(id) is None:
            return {"error": "failed to load model"}
    return {"model.id": id}


# simple unload model and save to state
@app.post("/v1/models/{id}:unload")
def unload_model(id: str):
    if app.state.models.get(id) is not None:
        del app.state.models[id]
        return {"model.id": id}
    return {"error": "model not found"}


# for starting server with script or directly
def main():
    import uvicorn  # unsure if this should import here or globally

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
