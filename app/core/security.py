import datetime as _dt
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    """Pydantic model for JWT payload data."""
    username: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if password matches hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[_dt.timedelta] = None) -> str:
    """
    Create a JWT token.
    The token will expire after the time defined in ACCESS_TOKEN_EXPIRE_MINUTES
    or after the provided expires_delta.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = _dt.datetime.now(_dt.timezone.utc) + expires_delta
    else:
        # Use the expiration time from settings
        expire = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify JWT token and extract the payload.
    Returns the token data on success, or None if validation fails.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            return None
        
        return TokenData(username=username)
    except JWTError:
        return None