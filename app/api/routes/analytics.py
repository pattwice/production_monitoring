from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from app.db.database import get_prod_db
from app.schemas import analytics as _schemas
from app.services.analytics_service import AnalyticsService
from app.api.routes.auth import get_current_user

router = _fastapi.APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/cycle-time", response_model=List[_schemas.FrontendCycleTime])
def get_ct_data(db: _orm.Session = _fastapi.Depends(get_prod_db), user = _fastapi.Depends(get_current_user)):
    """Returns data matching MOCK_CYCLE_TIME"""
    return AnalyticsService.get_cycle_time_table(db)

@router.get("/production-volume", response_model=List[_schemas.FrontendProductionVolume])
def get_pv_data(db: _orm.Session = _fastapi.Depends(get_prod_db), user = _fastapi.Depends(get_current_user)):
    """Returns data matching MOCK_PRODUCTION_VOLUME"""
    return AnalyticsService.get_production_volume(db)