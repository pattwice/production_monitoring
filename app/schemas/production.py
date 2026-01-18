import pydantic as _pd
import datetime as _dt
from typing import Optional as _Optional, List as _List

# --- STATION ---
class StationBase(_pd.BaseModel):
    station_code: str = _pd.Field(..., min_length=2, max_length=20)
    station_name: str = _pd.Field(..., min_length=3, max_length=100)
    description: _Optional[str] = None
    is_active: bool = True

class StationCreate(StationBase):
    pass

class StationResponse(StationBase):
    id: int
    created_at: _dt.datetime

    class Config:
        from_attributes = True

# --- WORK ELEMENT (Tasks) ---
class WorkElementBase(_pd.BaseModel):
    element_code: str
    element_name: str
    description: _Optional[str] = None
    sequence_order: int = 1

class WorkElementCreate(WorkElementBase):
    station_id: int

class WorkElementResponse(WorkElementBase):
    id: int
    station_id: int
    created_at: _dt.datetime

    class Config:
        from_attributes = True

# --- CYCLE TIME (Records) ---
class CycleTimeCreate(_pd.BaseModel):
    station_id: int
    work_element_id: int
    cycle_time: float
    cycle_number: int
    is_outlier: bool = False

class CycleTimeResponse(CycleTimeCreate):
    id: int
    recorded_at: _dt.datetime
    date_only: str

    class Config:
        from_attributes = True