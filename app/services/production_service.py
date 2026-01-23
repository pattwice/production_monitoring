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
        # Validate that the station ID exists
        station = db.query(_models.Station).filter(_models.Station.id == record.station_id).first()
        if not station:
            raise _fastapi.HTTPException(status_code=404, detail=f"Station with ID {record.station_id} not found.")

        # Validate that the work element ID exists
        work_element = db.query(_models.WorkElement).filter(_models.WorkElement.id == record.work_element_id).first()
        if not work_element:
            raise _fastapi.HTTPException(status_code=404, detail=f"Work Element with ID {record.work_element_id} not found.")

        today_str = _dt.datetime.now().strftime("%Y-%m-%d")
        db_record = _models.CycleTimeRecord(
            **record.model_dump(),
            date_only=today_str
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update_work_element_standard_time(db: _orm.Session, element_id: int, element_update: _schemas.WorkElementUpdate):
        db_element = db.query(_models.WorkElement).filter(_models.WorkElement.id == element_id).first()
        if not db_element:
            raise _fastapi.HTTPException(status_code=404, detail="Work Element not found")

        db.refresh(db_element)
        return db_element

    @staticmethod
    def get_standard_times_data(db: _orm.Session):
        """
        Fetches and structures standard time data for the frontend manager view.
        """
        stations = db.query(_models.Station).options(_orm.selectinload(_models.Station.work_elements)).all()
        
        response_data = {}
        for station in stations:
            station_tasks = []
            station_ct = 0
            for we in station.work_elements:
                station_tasks.append({
                    "id": we.id,
                    "task": we.element_name,
                    "standardCT": we.standard_time
                })
                station_ct += we.standard_time

            # The frontend has a concept of "Line" and "Station" being different,
            # but our model doesn't. For now, we'll treat the Station as the Line and also the Station.
            response_data[station.id] = {
                "line": station.station_name,
                "lineCT": round(station_ct, 2),
                "stations": {
                    station.id: {
                        "station": station.station_name,
                        "stationCT": round(station_ct, 2),
                        "tasks": station_tasks
                    }
                }
            }
        return response_data
