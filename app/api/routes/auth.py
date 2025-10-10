import datetime as _dt
import fastapi as _fastapi
import fastapi.security as _apiSecurity
import sqlalchemy.orm as _orm

from app.db.database import get_auth_db as _get_auth_db
from app.schemas.user import UserCreate as _UserCreate, UserResponse as _UserResponse, Token as _Token
from app.services.auth_service import AuthService as _AuthService
from app.core.security import create_access_token as _create_access_token, verify_token as _verify_token
from app.core.config import settings as _settings

router = _fastapi.APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = _apiSecurity.OAuth2PasswordBearer(tokenUrl=f"{_settings.API_V1_PREFIX}/auth/login")

@router.post("/register", response_model=_UserResponse, status_code=_fastapi.status.HTTP_201_CREATED)
def register(
    user_data: _UserCreate,
    db: _orm.Session = _fastapi.Depends(_get_auth_db)
    ):
    """
    Register a new user in AUTH database
    
    - **email**: Valid email address
    - **username**: 3-50 characters
    - **password**: Minimum 8 charactes
    - **full_name**: Optional
    """
    user = _AuthService.create_user(db, user_data)
    return user

@router.post("/login", response_model=_Token)
def login(
    form_data: _apiSecurity.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_get_auth_db)
):
    """
    Login to get acess token
    Send username and password to receive a JWT token
    """
    user = _AuthService.authentication_user(db, form_data.username, form_data.password)

    access_token_expires = _dt.timedelta(minutes=_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(
        token: str = _fastapi.Depends(oauth2_scheme),
        db: _orm.Session = _fastapi.Depends(_get_auth_db)
):
    """
    Dependency to get current authenticated user from AUTH database
    """
    username = _verify_token(token)
    if username is None:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = _AuthService.get_current_user(db, username)
    return user

@router.get("/me", response_model=_UserResponse)
def get_me(current_user = _fastapi.Depends(get_current_user)):
    """
    Get current user information.
    Requires authentication token.
    """
    return current_user