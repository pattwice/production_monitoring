import sqlalchemy.orm as _orm
import sqlalchemy as _sql
from app.models import production as _models
from app.schemas import analytics as _schemas

class AnalyticsService:

    @staticmethod
    def get_cycle_time_table(db: _orm.Session):
        # Join CycleTime -> Station -> WorkElement
        results = db.query(
            _models.CycleTimeRecord,
            _models.Station,
            _models.WorkElement
        ).select_from(_models.CycleTimeRecord).join(_models.Station).join(_models.WorkElement).all()

        output = []
        for record, station, element in results:
            # Logic for outlier: if marked as outlier, show the delta
            outlier_val = None
            if record.is_outlier:
                outlier_val = round(record.cycle_time - element.standard_time, 4)

            output.append(_schemas.FrontendCycleTime(
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