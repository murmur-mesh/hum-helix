from pydantic import BaseModel
from typing import Optional


# POST /v1/models/load
class LoadModelRequest(BaseModel):
    model: str
    device: str
    compute_type: str
    download_root: Optional[str] = None


# POST /v1/models/unload
class UnloadModelRequest(BaseModel):
    model: str
