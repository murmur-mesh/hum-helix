from typing import Dict
from fastapi import Request
from faster_whisper import WhisperModel


# this file is a shared dependency to avoid circular imports and to
# standardize access to application state for a request


def get_loaded_models(request: Request) -> Dict[str, WhisperModel]:
    return request.app.state.models
