from fastapi import FastAPI
from faster_whisper import WhisperModel

app = FastAPI()


# load a model
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# temporarily load whisper for test
@app.get("/load")
def load_model():
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    output = model.max_length
    return {"model.max_length": f"{output}"}


# wrap in api, manually load, simply return an echo
def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
