from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm

from app.db.database import get_prod_db
from app.schemas import production as _schemas
from app.services.production_service import ProductionService
from app.api.routes.auth import get_current_user, get_current_superuser

router = _fastapi.APIRouter(prefix="/production", tags=["Production Management"])

@router.post("/stations", response_model=_schemas.StationResponse, status_code=201)
def create_station(
    station: _schemas.StationCreate, 
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    return ProductionService.create_station(db, station)

@router.get("/stations", response_model=List[_schemas.StationResponse])
def list_stations(
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    return ProductionService.get_stations(db)

@router.get("/standard-times-data")
def get_standard_times_data(
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    return ProductionService.get_standard_times_data(db)

@router.post("/work-elements", response_model=_schemas.WorkElementResponse, status_code=201)
def create_work_element(
    element: _schemas.WorkElementCreate, 
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    return ProductionService.create_work_element(db, element)

@router.put("/work-elements/{element_id}", response_model=_schemas.WorkElementResponse)
def update_work_element(
    element_id: int,
    element_update: _schemas.WorkElementUpdate,
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_superuser)
):
    return ProductionService.update_work_element_standard_time(db, element_id, element_update)


@router.post("/cycles", response_model=_schemas.CycleTimeResponse, status_code=201)
def record_cycle(
    record: _schemas.CycleTimeCreate,
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    return ProductionService.record_cycle_time(db, record)

@router.get("/work-elements-info", response_model=List[_schemas.WorkElementInfo])
def get_work_elements_info_route(
    db: _orm.Session = _fastapi.Depends(get_prod_db),
    user = _fastapi.Depends(get_current_user)
):
    """
    Returns a list of work elements with their station names and sequence order.
    """
    return ProductionService.get_work_elements_info(db)