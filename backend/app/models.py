from pydantic import BaseModel
from typing import Optional

class SessionCreateResponse(BaseModel):
    session_id: str
    message: str

class SessionStatus(BaseModel):
    session_id: str
    status: str
    progress: int
    message: str
    created_at: str
    updated_at: str

class TemplateBbox(BaseModel):
    x: int
    y: int
    width: int
    height: int

class ProcessConfig(BaseModel):
    threshold: float = 0.8
    right_ratio: float = 0.6

class ProcessResult(BaseModel):
    success: bool
    message: str
    avatar_count: int
    result_url: Optional[str] = None