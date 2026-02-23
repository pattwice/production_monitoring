import sqlalchemy.orm as _orm
import sqlalchemy as _sql
from app.models import production as _models
from app.schemas import analytics as _schemas

class AnalyticsService:

    @staticmethod
    def get_cycle_time_table(db: _orm.Session, date: str = None):
        # Base query
        query = db.query(
            _models.CycleTimeRecord,
            _models.Station,
            _models.WorkElement
        ).select_from(_models.CycleTimeRecord).join(_models.Station).join(_models.WorkElement)

        # Apply date filter if provided
        if date:
            query = query.filter(_models.CycleTimeRecord.date_only == date)
        
        results = query.all()

        output = []
        for record, station, element in results:
            outlier_val = None
            if record.is_outlier:
                outlier_val = round(record.cycle_time - element.standard_time, 4)

            output.append(_schemas.FrontendCycleTime(
                cycleId=record.cycle_number,
                lineId=station.id,
                lineName=station.station_name,
                businessDate=record.date_only,
                shift=record.shift,
                station=station.station_name,
                operator=record.operator,
                task=element.element_name,
                ct=record.cycle_time,
                outlier=outlier_val,
                time=record.recorded_at.strftime("%H:%M"),
                standard=element.standard_time
            ))
        return output

    @staticmethod
    def get_cycle_time_by_task(db: _orm.Session, task: str, date: str = None):
        # Base query
        query = db.query(
            _models.CycleTimeRecord,
            _models.Station,
            _models.WorkElement
        ).select_from(_models.CycleTimeRecord)\
         .join(_models.Station, _models.CycleTimeRecord.station_id == _models.Station.id)\
         .join(_models.WorkElement, _models.CycleTimeRecord.work_element_id == _models.WorkElement.id)\
         .filter(_models.WorkElement.element_name == task)

        # Apply date filter if provided
        if date:
            query = query.filter(_models.CycleTimeRecord.date_only == date)
            
        results = query.all()

        output = []
        for record, station, element in results:
            outlier_val = None
            if record.is_outlier:
                outlier_val = round(record.cycle_time - element.standard_time, 4)

            output.append(_schemas.FrontendCycleTime(
                cycleId=record.cycle_number,
                lineId=station.id,
                lineName=station.station_name,
                businessDate=record.date_only,
                shift=record.shift,
                station=station.station_name,
                operator=record.operator,
                task=element.element_name,
                ct=record.cycle_time,
                outlier=outlier_val,
                time=record.recorded_at.strftime("%H:%M"),
                standard=element.standard_time
            ))
        return output

    @staticmethod
    def get_production_volume(db: _orm.Session):
        # This function provides aggregated hourly production volume.
        PLANNED_PER_HOUR = 72  # A reasonable target, e.g., 3600s in an hour / ~50s per full cycle

        # Group records by hour using PostgreSQL's date_trunc function
        results = (
            db.query(
                _models.Station.station_name,
                _models.CycleTimeRecord.date_only,
                _models.CycleTimeRecord.shift,
                _sql.func.date_trunc('hour', _models.CycleTimeRecord.recorded_at).label('hour_timestamp'),
                _sql.func.count(_models.CycleTimeRecord.id).label('actual_volume')
            )
            .join(_models.Station, _models.CycleTimeRecord.station_id == _models.Station.id)
            .group_by(
                'hour_timestamp',
                _models.Station.station_name,
                _models.CycleTimeRecord.date_only,
                _models.CycleTimeRecord.shift
            )
            .order_by('hour_timestamp')
            .all()
        )

        output = []
        for r in results:
            output.append(_schemas.FrontendProductionVolume(
                lineName=r.station_name,
                businessDate=r.date_only,
                shift=r.shift,
                time=r.hour_timestamp.strftime("%H:00"),  # Format to HH:00
                planned=PLANNED_PER_HOUR,
                actual=r.actual_volume
            ))
        return output

    @staticmethod
    def get_cycle_time_distribution(db: _orm.Session, task: str, date: str = None, bin_size: int = 5):
        """
        Calculates the frequency distribution for a given task's cycle times.
        """
        # First, get all the cycle time values (ct) for the given task and date
        query = db.query(_models.CycleTimeRecord.cycle_time)\
                  .join(_models.WorkElement)\
                  .filter(_models.WorkElement.element_name == task)
        
        if date:
            query = query.filter(_models.CycleTimeRecord.date_only == date)
            
        cycle_times = query.all()
        
        if not cycle_times:
            return []
            
        # Perform binning logic
        bins = {}
        for (ct,) in cycle_times:
            bucket = int(ct // bin_size) * bin_size
            label = f"{bucket}-{bucket + bin_size -1}"
            bins[label] = bins.get(label, 0) + 1
            
        # Format for response
        output = [
            _schemas.CycleTimeDistributionBin(ctRange=key, count=value)
            for key, value in bins.items()
        ]
        
        # Sort by the start of the range
        output.sort(key=lambda x: int(x.ctRange.split('-')[0]))
        
        return output

    @staticmethod
    def get_latest_data_date(db: _orm.Session):
        """
        Finds the most recent date in the cycle_time_records table.
        """
        latest_date = db.query(_sql.func.max(_models.CycleTimeRecord.date_only)).scalar()
        
        if latest_date:
            return {"latest_date": latest_date}
        
        # If no data exists, default to today's date
        from datetime import date
        return {"latest_date": date.today().isoformat()}

    @staticmethod
    def get_line_cycle_time(db: _orm.Session, line_name: str, date: str = None):
        """
        Calculates the total cycle time for each cycle number on a specific line.
        """
        # Step 1: Get the Standard CT for the line by summing standard times of all its work elements
        station = db.query(_models.Station).filter(_models.Station.station_name == line_name).first()
        if not station:
            return []
        
        standard_ct_query = db.query(_sql.func.sum(_models.WorkElement.standard_time))\
                                .filter(_models.WorkElement.station_id == station.id)
        total_standard_ct = standard_ct_query.scalar() or 0

        # Step 2: Get the actual CT by summing up records per cycle_number
        query = db.query(
            _models.CycleTimeRecord.cycle_number,
            _sql.func.sum(_models.CycleTimeRecord.cycle_time).label("actual_ct"),
            _sql.func.min(_models.CycleTimeRecord.recorded_at).label("time")
        ).filter(_models.CycleTimeRecord.station_id == station.id)

        if date:
            query = query.filter(_models.CycleTimeRecord.date_only == date)
        
        query = query.group_by(_models.CycleTimeRecord.cycle_number).order_by("time")
        
        results = query.all()

        # Step 3: Format the output
        output = [
            _schemas.FrontendCycleTime(
                cycleId=r.cycle_number,
                lineId=station.id,
                lineName=line_name,
                businessDate=date,
                shift="N/A", 
                station=line_name,
                operator="N/A",
                task="Overall",
                ct=r.actual_ct,
                time=r.time.strftime("%H:%M"),
                standard=total_standard_ct
            ) for r in results
        ]
        return output