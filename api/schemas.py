from pydantic import BaseModel
from typing import Optional

class PredictionResponse(BaseModel):
    score: float
    label: str
    catatan: Optional[str] = None