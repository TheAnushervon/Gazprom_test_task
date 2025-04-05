import datetime
from pydantic import BaseModel
from typing import Optional

class ReadingCreate(BaseModel):
    x: float
    y: float
    z: float

class ReadingResponse(BaseModel):
    id: int
    device_id: str
    timestamp: datetime.datetime
    x: float
    y: float
    z: float

    class Config:
        form_attributes = True
        

class AnalysisResult(BaseModel):
    count: int
    min_x: Optional[float] = None
    max_x: Optional[float] = None
    sum_x: Optional[float] = None
    median_x: Optional[float] = None
    min_y: Optional[float] = None
    max_y: Optional[float] = None
    sum_y: Optional[float] = None
    median_y: Optional[float] = None
    min_z: Optional[float] = None
    max_z: Optional[float] = None
    sum_z: Optional[float] = None
    median_z: Optional[float] = None