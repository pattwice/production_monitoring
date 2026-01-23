from typing import List
import datetime as _dt
import fastapi as _fastapi
import fastapi.security as _apiSecurity
import sqlalchemy.orm as _orm
import jwt as _jwt
from app.models import user as _models

from app.db.database import get_auth_db as _get_auth_db
from app.schemas.user import UserCreate, UserResponse, Token, TokenData, UserUpdate
from app.services.auth_service import AuthService
from app.core.security import create_access_token, verify_token
from app.core.config import settings

router = _fastapi.APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = _apiSecurity.OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

@router.post("/register", response_model=UserResponse, status_code=_fastapi.status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: _orm.Session = _fastapi.Depends(_get_auth_db)
):
    """
    Register a new user in AUTH database
    
    - **email**: Valid email address
    - **username**: 3-50 characters
    - **password**: Minimum 8 characters
    - **full_name**: Optional
    """
    user = AuthService.create_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: _apiSecurity.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_get_auth_db)
):
    """
    Login to get access token.
    Send username and password to receive a JWT token.
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)

    access_token_expires = _dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(
    token: str = _fastapi.Depends(oauth2_scheme),
    db: _orm.Session = _fastapi.Depends(_get_auth_db)
):
    """
    Decodes the JWT token and returns the corresponding user.
    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = _fastapi.HTTPException(
        status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = _jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except _jwt.PyJWTError:
        raise credentials_exception
    
    user = AuthService.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_superuser(current_user: _models.User = _fastapi.Depends(get_current_user)):
    """
    Checks if the current user is a superuser.
    If not, raises an HTTPException.
    """
    if not current_user.is_superuser:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges for this action.",
        )
    return current_user


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = _fastapi.Depends(get_current_user)):
    """
    Get current user information.
    Requires authentication token.
    """
    return current_user

@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    db: _orm.Session = _fastapi.Depends(_get_auth_db),
    user: _models.User = _fastapi.Depends(get_current_superuser)
):
    """
    Get a list of all users. Superuser access required.
    """
    return AuthService.get_users(db)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_roles(
    user_id: int,
    user_update: UserUpdate,
    db: _orm.Session = _fastapi.Depends(_get_auth_db),
    admin_user: _models.User = _fastapi.Depends(get_current_superuser)
):
    """
    Update a user's status and roles. Superuser access required.
    """
    return AuthService.update_user(db, user_id=user_id, user_data=user_update)
