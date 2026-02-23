from typing import List, Optional
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from app.db.database import get_prod_db
from app.schemas import analytics as _schemas
from app.services.analytics_service import AnalyticsService
from app.api.routes.auth import get_current_user
from datetime import datetime
import csv
from fastapi.responses import JSONResponse

router = _fastapi.APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/cycle-time", response_model=List[_schemas.FrontendCycleTime])
def get_ct_data(
    db: _orm.Session = _fastapi.Depends(get_prod_db), 
    user=_fastapi.Depends(get_current_user),
    task: Optional[str] = None,
    date: Optional[str] = None
):
    """
    Returns cycle time data.
    If 'task' query parameter is provided, filters data for that task.
    If 'date' query parameter is provided, filters data for that date.
    """
    if task:
        return AnalyticsService.get_cycle_time_by_task(db, task=task, date=date)
    
    return AnalyticsService.get_cycle_time_table(db, date=date)

@router.get("/production-volume", response_model=List[_schemas.FrontendProductionVolume])
def get_pv_data(db: _orm.Session = _fastapi.Depends(get_prod_db), user = _fastapi.Depends(get_current_user)):
    """Returns data matching MOCK_PRODUCTION_VOLUME"""
    return AnalyticsService.get_production_volume(db)

@router.get("/cycle-time-distribution", response_model=List[_schemas.CycleTimeDistributionBin])
def get_ct_distribution(
    db: _orm.Session = _fastapi.Depends(get_prod_db), 
    user=_fastapi.Depends(get_current_user),
    task: str = _fastapi.Query(..., description="The task name to calculate distribution for."),
    date: Optional[str] = None,
    bin_size: int = _fastapi.Query(1, description="The size of each bin for the histogram.")
):
    """
    Returns data for a frequency distribution histogram of cycle times.
    """
    return AnalyticsService.get_cycle_time_distribution(db, task=task, date=date, bin_size=bin_size)

@router.get("/latest-data-date")
def get_latest_date(
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user=_fastapi.Depends(get_current_user)
):
    """
    Returns the most recent date found in the cycle time records.
    """
    return AnalyticsService.get_latest_data_date(db)

@router.get("/line-cycle-time", response_model=List[_schemas.FrontendCycleTime])
def get_line_ct_data(
    db: _orm.Session = _fastapi.Depends(get_prod_db), 
    user=_fastapi.Depends(get_current_user),
    line_name: str = _fastapi.Query(..., description="The line name to fetch cycle times for."),
    date: Optional[str] = None
):
    """
    Returns aggregated cycle time data for a whole line.
    """
    return AnalyticsService.get_line_cycle_time(db, line_name=line_name, date=date)