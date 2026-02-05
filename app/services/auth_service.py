import sqlalchemy.orm as _orm
import fastapi as _fastapi

from app.models.user import User as _User
from app.schemas.user import UserCreate as _UserCreate
from app.core.security import get_hash_password as _get_hash_password, verify_password as _verify_password

class AuthService:
    """Handles all authentication logic"""

    @staticmethod
    def create_user(db: _orm.Session, user_data: _UserCreate) -> _User:
        """Create a new user in AUTH database"""
        # Check if already exists
        existing_user = db.query(_User).filter(
            (_User.email == user_data.email) | (_User.username == user_data.username)
        ).first()

        if existing_user:
            raise _fastapi.HTTPException(
                status_code=_fastapi.status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        db_user = _User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=_get_hash_password(user_data.password)
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: _orm.Session, username: str, password: str) -> _User:
        """Verify username and password from auth database"""
        user = db.query(_User).filter(_User.username == username).first()

        if not user or not _verify_password(password, user.hashed_password):
            # Combine user check and password verification for security
            raise _fastapi.HTTPException(
                status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}, # Standard for 401
            )
        
        if not user.is_active:
            raise _fastapi.HTTPException(
                status_code=_fastapi.status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        return user
    
    @staticmethod
    def get_users(db: _orm.Session):
        """Get all users from auth database"""
        return db.query(_User).all()

    @staticmethod
    def update_user(db: _orm.Session, user_id: int, user_data: _UserCreate) -> _User:
        """Update a user's details (is_active, is_superuser)"""
        db_user = db.query(_User).filter(_User.id == user_id).first()
        if not db_user:
            raise _fastapi.HTTPException(status_code=404, detail="User not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username(db: _orm.Session, username: str) -> _User:
        """Get user by username from auth database"""
        user = db.query(_User).filter(_User.username == username).first()
        
        if not user:
            raise _fastapi.HTTPException(
                status_code=_fastapi.status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
