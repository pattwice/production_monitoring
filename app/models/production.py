import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from sqlalchemy.sql import func as _func

from app.db.database import ProdBase as _ProdBase

class Station(_ProdBase):
    """
    Represents a production station.
    """
    __tablename__ = "stations"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    station_code = _sql.Column(_sql.String, unique=True, index=True, nullable=False)
    station_name = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)
    created_at = _sql.Column(_sql.DateTime(timezone=True), server_default=_func.now())

    # Realationship
    work_elements = _orm.relationship("WorkElement", back_populates="station")
    cycle_records = _orm.relationship("CycleTimeRecord", back_populates="station")

    def __repr__(self):
        return f"<Station(code='{self.station_code}', name='{self.station_name}')>"
    
class WorkElement(_ProdBase):
    """
    Represents a work element/task within a station.
    """
    __tablename__ = "work_elements"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    station_id = _sql.Column(_sql.Integer, _sql.ForeignKey("stations.id"), nullable=False)
    element_code = _sql.Column(_sql.String, index=True, nullable=False)
    element_name = _sql.Column(_sql.String, nullable=False)
    description = _sql.Column(_sql.String)
    sequence_order = _sql.Column(_sql.Integer)
    is_active = _sql.Column(_sql.Boolean, default=True)
    created_at = _sql.Column(_sql.DateTime(timezone=True), server_default=_func.now())

    # Relationships
    station = _orm.relationship("Station", back_populates="work_elements")
    cycle_records = _orm.relationship("CycleTimeRecord", back_populates="work_element")
    threshold = _orm.relationship("StatisticalThreshold", back_populates="work_element", uselist=False) # 1-to-1
    
    def __repr__(self):
        return f"<WorkElement(code='{self.element_code}', name='{self.element_name}')>"
    
class CycleTimeRecord(_ProdBase):
    """
    Stores actual cycle time measurments from 
    """
    __tablename__ = "cycle_time_records"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    station_id = _sql.Column(_sql.Integer, _sql.ForeignKey("stations.id"), nullable=False)
    work_element_id = _sql.Column(_sql.Integer, _sql.ForeignKey("work_elements.id"), nullable=False)
    
    # Cycle time data
    cycle_number = _sql.Column(_sql.Integer)
    cycle_time = _sql.Column(_sql.Float, nullable=False) # Seconds
    
    # Timestamp
    recorded_at = _sql.Column(_sql.DateTime(timezone=True), server_default=_func.now())
    date_only = _sql.Column(_sql.String, index=True)  # YYYY-MM-DD
    
    # Outlier detection
    is_outlier = _sql.Column(_sql.Boolean, default=False)
    
    # Relationships
    station = _orm.relationship("Station", back_populates="cycle_records")
    work_element = _orm.relationship("WorkElement", back_populates="cycle_records")
    
    def __repr__(self):
        return f"<CycleTimeRecord(cycle={self.cycle_number}, time={self.cycle_time}s)>"
    
class StatisticalThreshold(_ProdBase):
    """
    Stores statistical thresholds for each work element
    """
    __tablename__ = "statistical_thresholds"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    work_element_id = _sql.Column(_sql.Integer, _sql.ForeignKey("work_elements.id"), nullable=False)

    # Statistical Data
    avg_time = _sql.Column(_sql.Float, nullable=False)
    stdev_time = _sql.Column(_sql.Float)
    variance_time = _sql.Column(_sql.Float)
    lower_limit = _sql.Column(_sql.Float)
    upper_limit = _sql.Column(_sql.Float)
    
    # Metadata
    updated_at = _sql.Column(_sql.DateTime(timezone=True), server_default=_func.now(), onupdate=_func.now())

    # Relationship
    work_element = _orm.relationship("WorkElement", back_populates="threshold")

    def __repr__(self):
        return f"<Threshold(element_id={self.work_element_id}, avg={self.avg_time})>"