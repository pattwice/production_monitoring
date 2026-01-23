from pydantic import BaseModel, Field
from typing import List, Optional

# ============================================
# Station Schemas
# ============================================

class StationBase(BaseModel):
    station_code: str = Field(..., example="MP1")
    station_name: str = Field(..., example="Main Production Line 1")
    description: Optional[str] = None

class StationCreate(StationBase):
    pass

class StationResponse(StationBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# ============================================
# Work Element Schemas
# ============================================

class WorkElementBase(BaseModel):
    station_id: int
    element_code: str = Field(..., example="MP1-WE01")
    element_name: str = Field(..., example="Assembly the first sitepage")
    standard_time: float = Field(..., example=10.5)

class WorkElementCreate(WorkElementBase):
    pass

class WorkElementUpdate(BaseModel):
    standard_time: float = Field(..., example=12.0)

class WorkElementResponse(WorkElementBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

# ============================================
# Cycle Time Schemas
# ============================================

class CycleTimeBase(BaseModel):
    station_id: int
    work_element_id: int
    cycle_time: float
    cycle_number: Optional[int] = None
    is_outlier: Optional[bool] = False
    shift: Optional[str] = "Day"
    operator: Optional[str] = "Operator"

class CycleTimeCreate(CycleTimeBase):
    pass

class CycleTimeResponse(CycleTimeBase):
    id: int
    recorded_at: str 
    date_only: str

    class Config:
        orm_mode = True
