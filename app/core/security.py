import datetime as _dt
from typing import Optional as _Optional
from jose import JWTError as _JWTError, jwt as _jwt

from passlib.context import CryptContext as _CrypContext
from app.core.config import settings as _setttings

pwd_context = _CrypContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if password matches hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: _Optional[_dt.timedelta] = None) -> str:
    """Create a JWT token"""
    to_encode = data.copy()

    if expires_delta:
        expire = _dt.datetime.now(_dt.timezone.utc) + expires_delta
    else:
        expire = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = _jwt.encode(to_encode, _setttings.SECRET_KEY, algorithm=_setttings.ALGORITHM)
    return encode_jwt

def verify_token(token: str) -> _Optional[str]:
    """
    Verify JWT token and extract username
    Returns None if token is invalid
    """
    try:
        payload = _jwt.decode(token, _setttings.SECRET_KEY, algorithms=[_setttings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            return None
        
        return username
    except _JWTError:
        return None