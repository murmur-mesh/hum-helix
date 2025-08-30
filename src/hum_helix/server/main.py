import os
from fastapi import FastAPI, UploadFile, File
from contextlib import asynccontextmanager
from faster_whisper import WhisperModel
from pydantic import BaseModel
from typing import Optional

import tempfile, shutil

# pydantic hooks really well into fast api
from hum_helix.server.pydantic_types import LoadModelRequest, UnloadModelRequest

# router stuff
from hum_helix.server.routers import models, audio


# lifespan startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup initialize state
    app.state.models = {}
    yield
    # shutdown clear out state
    app.state.models = {}


app = FastAPI(lifespan=lifespan)

# setup routes with routers
app.include_router(models.router, prefix="/v1", tags=["models"])
app.include_router(audio.router, prefix="/v1", tags=["audio"])


# simple ping health check
@app.get("/ping")
def health_check():
    return {"status": "healthy"}


# for starting server with script or directly
def main():
    import uvicorn  # unsure if this should import here or globally

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
