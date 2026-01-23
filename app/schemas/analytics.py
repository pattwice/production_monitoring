import pydantic as _pd
from typing import Optional, List

class FrontendCycleTime(_pd.BaseModel):
    """Matches MOCK_CYCLE_TIME exactly"""
    lineId: int
    lineName: str
    businessDate: str
    shift: str
    station: str
    operator: str
    task: str
    ct: float
    outlier: Optional[float] = None
    time: str
    standard: float

class FrontendProductionVolume(_pd.BaseModel):
    """Matches MOCK_PRODUCTION_VOLUME exactly"""
    lineName: str
    businessDate: str
    shift: str
    time: str
    planned: int
    actual: int