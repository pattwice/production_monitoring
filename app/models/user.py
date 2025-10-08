import sqlalchemy as _sql
from sqlalchemy.sql import func as _func

from app.db.database import AuthBase  as _AuthBase

class User(_AuthBase):
    """
    User table in AUTHENTICATION database.
    Stores all user credentials and auth-related data.
    """
    __tablename__ = "users"
    
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True, nullable=False)
    username = _sql.Column(_sql.String, unique=True, index=True, nullable=False)
    hashed_password = _sql.Column(_sql.String, nullable=False)
    full_name = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)
    is_superuser = _sql.Column(_sql.Boolean, default=False)
    created_at = _sql.Column(_sql.DateTime(timezone=True), server_default=_func.now())
    updated_at = _sql.Column(_sql.DateTime(timezone=True), onupdate=_func.now())
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"