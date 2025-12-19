import sqlalchemy.orm as _orm
import datetime as _dt
import fastapi as _fastapi

from app.models import production as _models
from app.schemas import production as _schemas

class ProductionService:
    
    @staticmethod
    def create_station(db: _orm.Session, station: _schemas.StationCreate):
        # Prevent duplicate station codes
        existing = db.query(_models.Station).filter(_models.Station.station_code == station.station_code).first()
        if existing:
            raise _fastapi.HTTPException(status_code=400, detail="Station code already exists")
            
        db_station = _models.Station(**station.model_dump())
        db.add(db_station)
        db.commit()
        db.refresh(db_station)
        return db_station

    @staticmethod
    def get_stations(db: _orm.Session):
        return db.query(_models.Station).all()

    @staticmethod
    def create_work_element(db: _orm.Session, element: _schemas.WorkElementCreate):
        # Ensure station exists
        station = db.query(_models.Station).filter(_models.Station.id == element.station_id).first()
        if not station:
            raise _fastapi.HTTPException(status_code=404, detail="Station not found")
            
        db_element = _models.WorkElement(**element.model_dump())
        db.add(db_element)
        db.commit()
        db.refresh(db_element)
        return db_element

    @staticmethod
    def record_cycle_time(db: _orm.Session, record: _schemas.CycleTimeCreate):
        today_str = _dt.datetime.now().strftime("%Y-%m-%d")
        db_record = _models.CycleTimeRecord(
            **record.model_dump(),
            date_only=today_str
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record